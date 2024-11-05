import { Injectable } from '@angular/core';
import Web3 from 'web3';


const abiPath = 'assets/abi.json';
 const ContractAddress = "0x6287A7edF0298d2F95F507427A83910E24e6Aeca";
 const BlockchainUrl="http://127.0.0.1:8545";
 const GasLimit=6721975;
 const DummyAccountAddress="0xC6c62506828831A836bFf7925c25DEFc7BDCd0Fb";

@Injectable({
  providedIn: 'root',
})

export class Web3Service {
    private web3: any;
    private contract: any;

    constructor() {
      this.web3 = new Web3(new Web3.providers.HttpProvider(BlockchainUrl));

      //this.contract = new this.web3.eth.Contract(ABI, ContractAddress);

      fetch(abiPath)
          .then(response => response.json())
          .then(abiData => {
            this.contract = new this.web3.eth.Contract(abiData, ContractAddress);
            console.log(abiData);
            this.addCar("123456789", 2003);

          })
          .catch(error => {
            console.error('Error fetching ABI data:', error);
          });
    }

    startService() {
      this.addCar("123456789", 2003);

    }


    async getEvents() {
        return this.contract.methods.getEvents().call();
    }

    async getChassis() {
        return this.contract.methods.getChassis().call();
    }
    async getAccount(){
        return this.web3.eth.getAccounts();
    }
    addEvent(name: string, date: string) {

        this.contract.methods.addEvent(name, date).send({from: DummyAccountAddress, gas:GasLimit}).then((result: any) => {
            console.log("addEvent: ");
            console.log( result);
            return result
          },
          (error:any) => {
            console.log("error addEvent: ")
            console.log(error)
            throw error;
          }
        )

    }
/*
 function addCar(string memory chassisNumber, uint16 manufacturingYear) public {

        cars[chassisNumber] = new Car(chassisNumber, manufacturingYear);//msg.sender
    }

*/
    addCar(chassis: string, date: number) {

      this.contract.methods.addCar(chassis, date).send({from: DummyAccountAddress, gas:GasLimit}).then((result: any) => {
          console.log("add car: ");
          console.log( result);


          this.getCar("123456789");

          return result
        },
        (error:any) => {
          console.log("error add car: ")
          console.log(error)
          throw error;
        }
      )

  }

/*
 function getCar(string memory _chassisNumber) public view returns (Car){ // de aici vad toate detaliile masinii
        return cars[_chassisNumber];
    }

*/
  getCar(chassis: string) {

    this.contract.methods.getCar(chassis).call().then((result: any) => {
        console.log("get car: ");
        console.log( result);
        return result
      },
      (error:any) => {
        console.log("error get car: ")
        console.log(error)
        throw error;
      }
    )

}

}





const abi=[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "CarAdded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "propertyName",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "propertyValue",
				"type": "string"
			}
		],
		"name": "CarModified",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "eventType",
				"type": "string"
			}
		],
		"name": "EventAdded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "partName",
				"type": "string"
			}
		],
		"name": "PartAdded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "manufacturingYear",
				"type": "uint16"
			}
		],
		"name": "addCar",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "date",
				"type": "string"
			}
		],
		"name": "addEventToCar",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "chassisNumber",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "date",
				"type": "string"
			}
		],
		"name": "addModificationToCar",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_chassisNumber",
				"type": "string"
			}
		],
		"name": "getCar",
		"outputs": [
			{
				"components": [
					{
						"components": [
							{
								"internalType": "string",
								"name": "chassisNumber",
								"type": "string"
							},
							{
								"internalType": "uint16",
								"name": "manufacturingYear",
								"type": "uint16"
							}
						],
						"internalType": "struct CarInfo",
						"name": "carInfo",
						"type": "tuple"
					},
					{
						"components": [
							{
								"internalType": "string",
								"name": "name",
								"type": "string"
							},
							{
								"internalType": "string",
								"name": "date",
								"type": "string"
							}
						],
						"internalType": "struct Modification[]",
						"name": "modifications",
						"type": "tuple[]"
					},
					{
						"components": [
							{
								"internalType": "string",
								"name": "name",
								"type": "string"
							},
							{
								"internalType": "string",
								"name": "date",
								"type": "string"
							}
						],
						"internalType": "struct CarEvent[]",
						"name": "events",
						"type": "tuple[]"
					}
				],
				"internalType": "struct CarData",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
