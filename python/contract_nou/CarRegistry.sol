// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./Car.sol";

contract CarRegistry {
    mapping(string => Car) private cars;
    mapping(string => bool) private carExists; 
    string[] private carKeys;

    event LogEvent(uint256 indexed timestamp,uint256 indexed _number,string _message);
     
///////////////////////////////////////
    constructor(){
        emit LogEvent(block.timestamp, 0, "Car registry created");
    }

    function addChassis(uint64 _uid, string memory _ch) public {
        require(!carExists[_ch], "This chassis already exists");
        cars[_ch] = new Car(_uid,_ch);
        carExists[_ch] = true;
        carKeys.push(_ch);
    }

    function addDetails(
        uint64 _uid,
        string memory _ch,
        GeneralInfo memory _carInfo,
        EngineInfo memory _engineInfo,
        WheelsInfo memory _wheelsInfo) public {
        require(carExists[_ch], "Car does not exist");
        _carInfo.chassisNumber=_ch;
        cars[_ch].addDetails(_uid,  _carInfo, _engineInfo, _wheelsInfo);
    }

    function addWholeCar(uint64 _uid,
        GeneralInfo memory _carInfo,
        EngineInfo memory _engineInfo,
        WheelsInfo memory _wheelsInfo) public {

        string memory _ch = _carInfo.chassisNumber;
        require(!carExists[_ch], "This chassis already exists");
        cars[_ch] = new Car(_uid,_ch);
        carExists[_ch] = true;
        carKeys.push(_ch);
        cars[_ch].addDetails(_uid,  _carInfo, _engineInfo, _wheelsInfo);
    }

//////////////////////////////////////////
    function getCarInfo(string memory _ch) public view returns (GeneralInfo memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getCarInfo();
    }

   function getModificationHistory(string memory _ch) public view returns (Modification[] memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getModificationHistory();
    }

    function getEventHistory(string memory _ch) public view returns (CarEvent[] memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getEventHistory();
    }
    function getEngineInfo(string memory _ch) public view returns (EngineInfo memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getEngineInfo();
    }
    function getWheelsInfo(string memory _ch) public view returns (WheelsInfo memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getWheelsInfo();
    }
    function getExtra(string memory _ch) public view returns (Extra[] memory) {
        require(carExists[_ch], "Car does not exist");
        return cars[_ch].getExtras();
    }

    function getChassis() public view returns (string[] memory){
        return carKeys;
    }
    function getTransfer(string memory _ch) public view returns (string memory){
        require(carExists[_ch], "Car does not exist");
        if (cars[_ch].getTransferedState() == true){
            return cars[_ch].getTransferChassis();
        }
        return "" ;
    }
//////////////////////////////////////
    function addModification(uint256 timestamp,uint64 _uid, string memory _ch, Part _modificationEnum, string memory _details) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].addModification( timestamp,_uid, _modificationEnum, _details);
    }

    function addEvent(uint256 timestamp,uint64 _uid, string memory chassisNumber, EventName _eventEnum, string memory _details) public {
        require(carExists[chassisNumber], "Car does not exist");
        cars[chassisNumber].addEvent( timestamp,_uid, _eventEnum, _details);
    }
    function addExtra(uint256 timestamp,uint64 _uid, string memory _ch, string memory _details) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].addExtra(timestamp,_uid, _details);
    }

    function addTransfer(uint256 timestamp,uint64 _uid, string memory _ch, string memory _newChassis) public {
        require(carExists[_ch], "Car does not exist");
        require(keccak256(abi.encodePacked(_ch)) != keccak256(abi.encodePacked(_newChassis)), "Chassis must be different");
        cars[_ch].addTransfer(timestamp,_uid,  _newChassis);
        addChassis(_uid, _newChassis);
//        GeneralInfo memory _carInfo = cars[_ch].getCarInfo();
//        _carInfo.chassisNumber=_newChassis;
//        addDetails(_uid,_newChassis, _carInfo, EngineInfo('','',0,''), WheelsInfo(0,0,0));
    }
//////////////////////////////////////
    function modifyKm(uint256 timestamp,uint64 _uid, string memory _ch, uint32 _nokm) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyKm( timestamp,_uid, _nokm);
    }

    function modifyBodyType(uint256 timestamp,uint64 _uid, string memory _ch, string memory _body) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyBodyType( timestamp,_uid, _body);
    }

    function modifyGearbox(uint256 timestamp,uint64 _uid, string memory _ch, string memory _gearbox) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyGearbox( timestamp,_uid, _gearbox);
    }

    function modifyColor(uint256 timestamp,uint64 _uid, string memory _ch, string memory _color) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyColor( timestamp,_uid, _color);
    }

    function modifyNoSeats(uint256 timestamp,uint64 _uid, string memory _ch, uint32 _noSeats) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyNoSeats( timestamp,_uid, _noSeats);
    }

    function modifyNoDoors(uint256 timestamp,uint64 _uid, string memory _ch, uint32 _noDoors) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyNoDoors( timestamp,_uid, _noDoors);
    }

    function modifyTransmission(uint256 timestamp,uint64 _uid, string memory _ch, string memory _transmission) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyTransmission( timestamp,_uid, _transmission);
    }

    function modifyEngine(uint256 timestamp,uint64 _uid, string memory _ch, string memory _serial, string memory _liters, uint32 _hp, string memory _fuelType) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyEngine( timestamp,_uid, _serial, _liters, _hp, _fuelType);
    }

    function modifyWheels(uint256 timestamp,uint64 _uid, string memory _ch, uint32 _noWheels, uint32 _diameter, uint32 _width) public {
        require(carExists[_ch], "Car does not exist");
        cars[_ch].modifyWheels( timestamp,_uid, _noWheels, _diameter, _width);
    }

   
}