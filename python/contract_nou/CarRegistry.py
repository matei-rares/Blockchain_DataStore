import json
from datetime import datetime

from web3 import Web3, exceptions
from CustomException import CustomException
from solcx import install_solc, compile_files


def convert_tuple_to_json_general_info(data):
    keys = ['chassisNumber', 'manufacturingYear', 'manufacturer', 'model', 'bodyType', 'gearbox', 'color', 'noSeats',
            'noDoors', 'noKm', 'transmission']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_tuple_to_json_engine_info(data):
    keys = ['serial', 'liters', 'horsepower', 'fuelType']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_tuple_to_json_wheels_info(data):
    keys = ['noWheels', 'diameter', 'width']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_tuple_to_json_extra(data):
    print(data)
    keys = ['timestamp','id', 'details']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_tuple_to_json_modification(data):
    keys = ['timestamp', 'userId', 'partEnum', 'details']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_tuple_to_json_event(data):
    keys = ['timestamp', 'userId', 'eventEnum', 'details']
    result = dict(zip(keys, data))
    return json.loads(json.dumps(result))


def convert_json_general_info_to_tuple(data):
    return data['chassisNumber'], int(data['manufacturingYear']), data['manufacturer'], data['model'], data['bodyType'], \
        data['gearbox'], data['color'], int(data['noSeats']), int(data['noDoors']), int(data['noKm']), data[
        'transmission']


def convert_json_engine_info_to_tuple(data):
    return data['serial'], str(data['liters']), int(data['horsepower']), data['fuelType']


def convert_json_wheels_info_to_tuple(data):
    return int(data['noWheels']), int(data['diameter']), int(data['width'])


def convert_json_extra_to_tuple(data):
    return data['id'], data['details']


import security.secrets_reader as secrets
import hashlib


def get_file_hash(file_path):
    hash_func = getattr(hashlib, "sha256")()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


import subprocess


class CarRegistry:
    # TODO aduaga parte de gestionare useri
    GANACHE_URL = "http://127.0.0.1:8545"
    # GAS_PRICE = Web3(Web3.HTTPProvider(GANACHE_URL)).to_wei('20', 'gwei')
    # GAS_LIMIT = 600000000
    CONTRACT_ADDRESS = secrets.get_secret(secrets.Keys.CONTRACT_ADDRESS)
    PRIVATE_KEY = secrets.get_secret(secrets.Keys.PRIVATE_KEY)
    file = "contract_nou/"
    pre = file
    ABI_FILE_PATH = pre + "CarRegistry_sol_CarRegistry.abi"
    CONTRACT1_PATH = pre + "Car.sol"
    CONTRACT2_PATH = pre + "CarRegistry.sol"

    def __init__(self):
        self.contract = None
        self.web3 = Web3(Web3.HTTPProvider(self.GANACHE_URL))
        if self.web3.is_connected():
            print("Ganache Conectat!")
        else:
            print("Eroare conectare Ganache!")
            exit()

        redeploy = self.check_files_and_compile()

        start = False
        while not start:
            with open(self.ABI_FILE_PATH, "r") as abi_file:
                self.contract_abi = json.load(abi_file)
            try:
                self.contract = self.web3.eth.contract(address=self.CONTRACT_ADDRESS, abi=self.contract_abi)
                print(self.get_chassies())

                if redeploy:
                    self.deploy_and_save()
                    redeploy = False
                else:
                    start = True
            except Exception as e:
                if type(e) == exceptions.InvalidAddress or type(e) == exceptions.BadFunctionCallOutput:
                    self.deploy_and_save()
                else:
                    print("Error: ", e)
                    exit()

    def check_files_and_compile(self):
        self.default_account = self.get_default_account()
        self.ensure_balance()
        contract1_hash_file = secrets.get_secret(secrets.Keys.CONTRACT1_HASH)
        contract2_hash_file = secrets.get_secret(secrets.Keys.CONTRACT2_HASH)
        abi_hash_file = secrets.get_secret(secrets.Keys.ABI_FILE_HASH)

        contract1_hash_computed = get_file_hash(self.CONTRACT1_PATH)
        contract2_hash_computed = get_file_hash(self.CONTRACT2_PATH)
        abi_hash_computed = get_file_hash(self.ABI_FILE_PATH)

        recompiled = False
        if contract1_hash_file != contract1_hash_computed or contract2_hash_file != contract2_hash_computed or abi_hash_file != abi_hash_computed:
            print("Fisierele contractului sunt schimbate")
            # fisier modificat, trebuie recompilat

            # print(subprocess.run("where solcjs"))
            # calea catre biblioteca
            solcjs = secrets.get_secret(secrets.Keys.SOLCX_PATH)
            command = [solcjs, "--optimize", "--abi", "--bin", "-o", ".", "CarRegistry.sol"]
            result = subprocess.run(command)

            # print("stdout:", result)
            secrets.update_secret(secrets.Keys.CONTRACT1_HASH, contract1_hash_computed)
            secrets.update_secret(secrets.Keys.CONTRACT2_HASH, contract2_hash_computed)
            secrets.update_secret(secrets.Keys.ABI_FILE_HASH, abi_hash_computed)

            recompiled = True
        return recompiled

    def deploy_and_save(self):
        self.contract = self.compile_and_deploy()
        secrets.update_secret(secrets.Keys.CONTRACT_ADDRESS, self.contract)
        self.CONTRACT_ADDRESS = self.contract

    def compile_and_deploy(self):
        install_solc("0.8.0")
        compiled = compile_files(["Car.sol", "CarRegistry.sol"],
                                 solc_version="0.8.0",
                                 optimize=True)
        bin = compiled["CarRegistry.sol:CarRegistry"]["bin"]
        abi = json.loads(compiled["CarRegistry.sol:CarRegistry"]["metadata"])["output"]["abi"]
        chain_id = 1337
        new_contract = self.web3.eth.contract(abi=abi, bytecode=bin)
        transaction = new_contract.constructor().build_transaction(
            {
                "chainId": chain_id,
                "gasPrice": self.web3.eth.gas_price,
                "from": self.default_account,
                "nonce": self.web3.eth.get_transaction_count(self.default_account),
            }
        )
        t_hash, _ = self.sign_and_send_transaction(transaction)
        transaction_receipt = self.web3.eth.wait_for_transaction_receipt(t_hash)
        print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
        return transaction_receipt.contractAddress

    def get_default_account(self):
        default_account = self.web3.eth.default_account
        if not default_account:
            accounts = self.web3.eth.accounts
            for account in accounts:
                balance = self.web3.eth.get_balance(account)
                balance_in_ether = self.web3.from_wei(balance, 'ether')
                if balance_in_ether >= 5:
                    self.web3.eth.default_account = account
                    return account
        return default_account

    def ensure_balance(self):
        if self.default_account:
            balance = self.web3.eth.get_balance(self.default_account)
            balance_in_ether = self.web3.from_wei(balance, 'ether')
            if balance_in_ether < 5:
                amount_to_send = self.web3.to_wei(100 - balance_in_ether, 'ether')
                self.web3.eth.send_transaction(
                    {'to': self.default_account, 'from': self.web3.eth.coinbase, 'value': amount_to_send})
                print("Added Ether to default account.")
            else:
                print("Default account has sufficient balance.")
        else:
            print("No account found with sufficient balance.")

    def get_transaction_object(self):
        nonce = self.web3.eth.get_transaction_count(self.default_account)
        return {'from': self.default_account,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': nonce,
                }
        # 'limit': self.GAS_LIMIT,

    def sign_and_send_transaction(self, transaction):
        signed_transaction = self.web3.eth.account.sign_transaction(transaction, self.PRIVATE_KEY)
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return transaction_hash, transaction_hash.hex()
        # todo daca e nevoie de detalii despre tranzactie
        #  transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)
        print(self.web3.eth.wait_for_transaction_receipt(transaction_hash))

    def check_car_existence(self, chassis):
        if chassis in self.get_chassies():
            return True
        raise CustomException("Car not found", 404)

    def check_duplicate_chassis(self, chassis):
        chassies = self.get_chassies()
        if chassis in chassies:
            raise CustomException("Car already exists", 409)
        return True

    ###############################################GET#############################################################
    def get_car_info(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getCarInfo(chassis).call()
        return convert_tuple_to_json_general_info(result)

    def get_engine_info(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getEngineInfo(chassis).call()
        return convert_tuple_to_json_engine_info(result)

    def get_wheels_info(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getWheelsInfo(chassis).call()
        return convert_tuple_to_json_wheels_info(result)

    def get_extra(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getExtra(chassis).call()
        for i in range(len(result)):
            result[i] = convert_tuple_to_json_extra(result[i])
        return result

    def get_modification_history(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getModificationHistory(chassis).call()
        for i in range(len(result)):
            result[i] = convert_tuple_to_json_modification(result[i])
        return result

    def get_event_history(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getEventHistory(chassis).call()
        for i in range(len(result)):
            result[i] = convert_tuple_to_json_event(result[i])
        return result

    def get_chassies(self):
        result = self.contract.functions.getChassis().call()
        return result

    def get_transfer(self, chassis):
        self.check_car_existence(chassis)
        result = self.contract.functions.getTransfer(chassis).call()
        return result

    def get_car_all_info(self, chassis):
        self.check_car_existence(chassis)
        car_info = self.get_car_info(chassis)
        engine_info = self.get_engine_info(chassis)
        wheels_info = self.get_wheels_info(chassis)
        extra = self.get_extra(chassis)
        modification_history = self.get_modification_history(chassis)
        event_history = self.get_event_history(chassis)
        transfer = self.get_transfer(chassis)
        return {
            "carInfo": car_info,
            "engineInfo": engine_info,
            "wheelsInfo": wheels_info,
            "modificationHistory": modification_history,
            "eventHistory": event_history,
            "extra": extra,
            "transfer": transfer,
            "reversedOdometer": self.is_odometer_reverted(modification_history)
        }

    def is_odometer_reverted(self, modification_history):
        data = [entry for entry in modification_history if entry['partEnum'] == 0]
        for i in range(1, len(data)):
            prev_km = int(data[i - 1]['details'].split()[-3])
            curr_km = int(data[i]['details'].split()[-3])
            if curr_km < prev_km:
                return True
        return False

    def average_stats(self, manufacturingYear=0, event_history=[]):
        c_crashes, c_damages, c_sales, c_services, c_mentenances = 0, 0, 0, 0, 0
        years = 1
        if manufacturingYear != 0:
            years = datetime.now().year - manufacturingYear
        else:
            for event in event_history:
                if event['eventEnum'] == 9:
                    timestamp = event['timestamp']
                    timestamp_dt = datetime.fromtimestamp(timestamp)
                    years = 1 if timestamp_dt.year == 0 else years
                    print(years)
                    break

        c_crashes = sum(1 for item in event_history if item['eventEnum'] == 0) / years
        c_damages = sum(1 for item in event_history if item['eventEnum'] == 2) / years
        c_sales = sum(1 for item in event_history if item['eventEnum'] == 6) / years
        c_services = sum(1 for item in event_history if item['eventEnum'] == 7) / years
        c_mentenances = sum(1 for item in event_history if item['eventEnum'] == 8) / years

        return {"avg_crashes": c_crashes,
                "avg_damages": c_damages,
                "avg_sales": c_sales,
                "avg_services": c_services,
                "avg_mentenances": c_mentenances}

        ###############################################GET#############################################################

    # //mappingul imi da adresa, dar daca fac cars["key"].metoda  va accesa metoda corekta
    ################################################ADD############################################################
    def add_chassis(self, userid, chassis):
        if chassis in self.get_chassies():
            raise CustomException("Car already exists", 409)
        transaction = self.contract.functions.addChassis(userid, chassis).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_details(self, userid, chassis, general_info, engine_info, wheels_info):
        self.check_car_existence(chassis)
        general_info_tuple = convert_json_general_info_to_tuple(general_info)
        engine_info_tuple = convert_json_engine_info_to_tuple(engine_info)
        wheels_info_tuple = convert_json_wheels_info_to_tuple(wheels_info)
        transaction = self.contract.functions.addDetails(userid, chassis, general_info_tuple, engine_info_tuple,
                                                         wheels_info_tuple).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_whole_car(self, userid, general_info, engine_info, wheels_info):
        chassis = general_info['chassisNumber']
        self.check_duplicate_chassis(chassis)
        general_info_tuple = convert_json_general_info_to_tuple(general_info)
        engine_info_tuple = convert_json_engine_info_to_tuple(engine_info)
        wheels_info_tuple = convert_json_wheels_info_to_tuple(wheels_info)
        transaction = self.contract.functions.addWholeCar(userid, general_info_tuple, engine_info_tuple,
                                                          wheels_info_tuple).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_transfer(self, userId, chassis, newChassis, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addTransfer(timestamp, userId, chassis, newChassis).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

        general = self.get_car_info(chassis)
        engine = self.get_engine_info(chassis)
        wheels = self.get_wheels_info(chassis)
        self.add_details(userId, newChassis, general, engine, wheels)
        return

    def add_modification(self, userid, chassis, partEnum, details, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addModification(timestamp, userid, chassis, partEnum,
                                                              details).build_transaction(self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_event(self, userid, chassis, eventEnum, details, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addEvent(timestamp, userid, chassis, eventEnum,
                                                       details).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_extra(self, userid, chassis, details, timestamp=0):
        self.check_car_existence(chassis)
        # todo

        transaction = self.contract.functions.addExtra(timestamp, userid, chassis, details).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_cars_bulk(self, file):
        # todo de adaugat evenimente si modificari
        with open(file, "r") as file:
            data = file.read()
            _, data = data.split("++++++")
            cars = data.split("-----------------------")[0:-1]
            chassis = []
            i = 0
            n = 3
            for car in cars:

                if i > n:
                    pass
                clusters = car.split("\n")[1:-1]
                print(clusters)
                general_info = ()
                for i, item in enumerate(clusters[0].split("|")):
                    if i in [1, 7, 8, 9]:
                        item = int(item)
                    general_info += (item,)
                engine_info = ()
                for i, item in enumerate(clusters[1].split("|")):
                    if i in [2]:
                        item = int(float(item))
                    engine_info += (item,)
                wheels_info = ()
                for i, item in enumerate(clusters[2].split("|")):
                    item = int(float(item))
                    wheels_info += (item,)
                # print(general_info)
                # print(engine_info)
                # print(wheels_info)

                self.sign_and_send_transaction(
                    self.contract.functions.addWholeCar(0, general_info, engine_info, wheels_info).build_transaction(
                        self.get_transaction_object()))
                i += 1
            #     print(general_info[0])
            #     chassis+=[general_info[0],]
            # print(chassis)
            # counts={}
            # for item in chassis:
            #     counts[item] = counts.get(item, 0) + 1
            # num_duplicates = sum(count > 1 for count in counts.values())
            # print("Number of duplicates:", num_duplicates)

            print(len(cars))

    ################################################ADD############################################################

    ################################################MODIFY###########################################################

    def modify_km(self, userId, chassis, km, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyKm(timestamp, userId, chassis, km).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_gearbox(self, userId, chassis, gearbox, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyGearbox(timestamp, userId, chassis, gearbox).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_color(self, userId, chassis, color, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyColor(timestamp, userId, chassis, color).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_no_seats(self, userId, chassis, no_seats, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyNoSeats(timestamp, userId, chassis, no_seats).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_no_doors(self, userId, chassis, no_doors, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyNoDoors(timestamp, userId, chassis, no_doors).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_transmission(self, userId, chassis, transmission, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyTransmission(timestamp, userId, chassis,
                                                                 transmission).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_engine(self, userId, chassis, serial, liters, horsepower, fuel_type, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyEngine(timestamp, userId, chassis, serial, str(liters), horsepower,
                                                           fuel_type).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)

    def modify_wheels(self, userId, chassis, no_wheels, diameter, width, timestamp=0):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyWheels(timestamp, userId, chassis, no_wheels, diameter,
                                                           width).build_transaction(
            self.get_transaction_object())
        self.sign_and_send_transaction(transaction)


################################################MODIFY###########################################################

def tstr():
    car = CarRegistry()
    chas = '12345678'
    # car.add_chassis(0,chas)
    # car.add_transfer(0,chas,"90000")
    # car.add_cars_bulk("bulk.txt")
    # print(car.add_transfer(0,0,chas,"90000"))
    # print(car.get_transfer(chas))
    # print(car.get_car_info("90000"))
    # print(car.get_car_all_info(chas))
    # print(car.get_event_history(chas))
    # print(car.average_stats(0,car.get_event_history(chas)))
    # car.add_whole_car(0,{"chassisNumber":"000000"},0,0)
    pass


#tstr()
