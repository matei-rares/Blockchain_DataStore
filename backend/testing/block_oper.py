import json
import time

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
    keys = ['id', 'details']
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
    return data['chassisNumber'], data['manufacturingYear'], data['manufacturer'], data['model'], data['bodyType'], \
        data['gearbox'], data['color'], data['noSeats'], data['noDoors'], data['noKm'], data['transmission']


def convert_json_engine_info_to_tuple(data):
    return data['serial'], data['liters'], data['horsepower'], data['fuelType']


def convert_json_wheels_info_to_tuple(data):
    return data['noWheels'], data['diameter'], data['width']


def convert_json_extra_to_tuple(data):
    return data['id'], data['details']


class CarRegistry:
    # TODO aduaga parte de gestionare useri
    def __init__(self, url, contract_address, private_key):
        self.GANACHE_URL = url
        self.CONTRACT_ADDRESS = contract_address
        self.PRIVATE_KEY = private_key
        self.ABI_FILE_URL = "../contract_vechi/CarRegistry_sol_CarRegistry.abi"
        self.web3 = Web3(Web3.HTTPProvider(self.GANACHE_URL))

        with open(self.ABI_FILE_URL, "r") as abi_file:
            self.contract_abi = json.load(abi_file)
        if self.web3.is_connected():
            print("Connected to Ganache!")
        else:
            print("Not connected to Ganache. Please check your Ganache instance.")
            exit()
        print(self.web3.eth.default_account)
        self.default_account = self.get_default_account()
        print(self.default_account)
        self.ensure_balance()
        try:
            self.contract = self.web3.eth.contract(address=self.CONTRACT_ADDRESS, abi=self.contract_abi)
            print(self.get_chassies())
        except Exception as e:
            if type(e) == exceptions.InvalidAddress or type(e) == exceptions.BadFunctionCallOutput:
                self.contract = self.deploy()
                print("Contract deployed at address: ", self.contract)
                update_secret(Keys.CONTRACT_ADDRESS, self.contract)
            else:
                print("Error: ", e)
                exit()
        self.test()

    def deploy(self):
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
        return {
            'from': self.default_account,
            # 'gas': self.GAS_LIMIT,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': nonce,
        }

    def sign_and_send_transaction(self, transaction):
        signed_transaction = self.web3.eth.account.sign_transaction(transaction, self.PRIVATE_KEY)
        transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # todo daca e nevoie de detalii despre tranzactie
        #  transaction_receipt = self.web3.eth.wait_for_transaction_receipt(transaction_hash)
        return transaction_hash, transaction_hash.hex()

    def check_car_existence(self, chassis):
        chassies = self.get_chassies()
        if chassis in chassies:
            return True
        raise CustomException("Car not found", 404)

    def check_duplicate_chassis(self, chassis):
        chassies = self.get_chassies()
        if chassis in chassies:
            raise CustomException("Car already exists", 409)
        return True

    ############################################################################################################
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

    def get_car_all_info(self, chassis):
        self.check_car_existence(chassis)
        car_info = self.get_car_info(chassis)
        engine_info = self.get_engine_info(chassis)
        wheels_info = self.get_wheels_info(chassis)
        extra = self.get_extra(chassis)
        modification_history = self.get_modification_history(chassis)
        event_history = self.get_event_history(chassis)
        return {
            "carInfo": car_info,
            "engineInfo": engine_info,
            "wheelsInfo": wheels_info,
            "modificationHistory": modification_history,
            "eventHistory": event_history,
            "extra": extra
        }

    ############################################################################################################

    ############################################################################################################
    def add_chassis(self, userid, chassis):
        if self.check_car_existence(chassis) == True:
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

    def add_modification(self, userid, chassis, partEnum, details):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addModification(userid, chassis, partEnum, details).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_event(self, userid, chassis, eventEnum, details):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addEvent(userid, chassis, eventEnum, details).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_extra(self, userid, chassis, details):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.addExtra(userid, chassis, details).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def add_cars_bulk(self, file, start=0, stop=-1):
        # todo de terminat asta pentru a popula
        addresses = []
        with open(file, "r") as file:
            data = file.read()
            _, data = data.split("++++++")
            cars = data.split("-----------------------")[start:stop]

            chassis = []
            for car in cars:
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
                print(general_info)
                print(engine_info)
                print(wheels_info)

                # addresses.append(self.sign_and_send_transaction(
                #     self.contract_vechi.functions.addWholeCar(0, general_info, engine_info, wheels_info).build_transaction(
                #         self.get_transaction_object())))

            #     print(general_info[0])
            #     chassis+=[general_info[0],]
            # print(chassis)
            # counts={}
            # for item in chassis:
            #     counts[item] = counts.get(item, 0) + 1
            # num_duplicates = sum(count > 1 for count in counts.values())
            # print("Number of duplicates:", num_duplicates)

            print(len(cars))
        return addresses

    ############################################################################################################

    ############################################################################################################

    def modify_km(self, userid, chassis, km):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyKm(userid, chassis, km).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_gearbox(self, userid, chassis, gearbox):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyGearbox(userid, chassis, gearbox).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_color(self, userid, chassis, color):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyColor(userid, chassis, color).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_no_seats(self, userid, chassis, no_seats):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyNoSeats(userid, chassis, no_seats).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_no_doors(self, userid, chassis, no_doors):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyNoDoors(userid, chassis, no_doors).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_transmission(self, userid, chassis, transmission):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyTransmission(userid, chassis, transmission).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_engine(self, userid, chassis, serial, liters, horsepower, fuel_type):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyEngine(userid, chassis, serial, liters, horsepower,
                                                           fuel_type).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def modify_wheels(self, userid, chassis, no_wheels, diameter, width):
        self.check_car_existence(chassis)
        transaction = self.contract.functions.modifyWheels(userid, chassis, no_wheels, diameter,
                                                           width).build_transaction(
            self.get_transaction_object())
        return self.sign_and_send_transaction(transaction)

    def test(self):
        print(self.get_chassies())

    # self.add_cars_bulk(f'D:/an4/zzlic/python/repo/bulk.txt',1)
    def get_def_acc_address(self):
        return self.default_account


############################################################################################################
from security.secrets_reader import *

if __name__ == "__main__":
    car = CarRegistry("http://127.0.0.1:7545", get_secret(Keys.CONTRACT_ADDRESS),
                      "0x0dc301b196985cb3c77bb39143d677f82b8b17ba3d0a6684ae9dce56f90e5c57")

    while True:
        #inp = input("Enter something: ")
        inp="chas"
        if inp == "exit":
            break
        elif inp == "add":
            print(car.add_chassis(0, "123"))
        elif inp == "add_det":
            print(car.add_details(0, "123", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), (1, 2, 3, 4), (1, 2, 3)))
        elif inp == "add_whole":
            print(car.add_whole_car(0, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), (1, 2, 3, 4), (1, 2, 3)))
        elif inp == "bulk":
            print(car.add_cars_bulk("D:/an4/zzlic/python/repo/bulk.txt", 0, 1))
        elif inp == "chas":
            print(car.get_chassies())
        elif inp == "addr":
            print(car.get_def_acc_address())
        elif inp == "cont":
            print(car.CONTRACT_ADDRESS)
        elif inp == "minute":
            start_time = time.time()
            end_time = start_time + 60
            km = 25001
            i = 0
            while time.time() < end_time:
                car.modify_km(0, '1ABC2345', km)
                km += 1
                i += 1
            print(km)
            print("changes", i)
        else:
            data = car.get_car_all_info(inp)

            print(json.dumps(
                {"carInfo": data["carInfo"],
                 "engineInfo": data["engineInfo"],
                 "wheelsInfo": data["wheelsInfo"]
                 }, indent=4))
