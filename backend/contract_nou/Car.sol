// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//*  Daca folosesc clase toate metodele care adauga proprietati ale masinii trebuie sa aiba parametrii acelei proprietati ca sa o instantieze si sa o adauge in array

contract Car {
    GeneralInfo private currentCarInfo;
    Modification[] private modificationHistory;
    CarEvent[] private eventHistory;
    EngineInfo private engineInfo;
    WheelsInfo private wheelsInfo;
    Extra[] private extras;
    string private transfer="";
    bool private isTransfered=false;
    bool private isRegistered=false;

/////////////////////////initalizare
    constructor(uint64 _uid,string memory _chassis) {
        currentCarInfo.chassisNumber=_chassis;
        addEvent(0,_uid,EventName.Register, string(abi.encodePacked("Car registered in the system with chassis ",_chassis)));
    }

     function addDetails(
        uint64 _uid,
        GeneralInfo memory c,
        EngineInfo memory e,
        WheelsInfo memory w
    ) public {
        require(!isRegistered, "This car is already registered");
        addEvent(0, _uid, EventName.Register, string(abi.encodePacked("General info added:",
            "year: ", uint32ToString(c.manufacturingYear), ", manufacturer: ", c.manufacturer, ", model: ", c.model)));

        currentCarInfo = c;
        engineInfo = e;
        wheelsInfo = w;
        isRegistered = true;
    }
//////////////////////////


   //////////////////gettere
    function getCarInfo() public view returns (GeneralInfo memory) {
        return currentCarInfo;
    }
    function getEngineInfo() public view returns (EngineInfo memory) {
        return engineInfo;
    }
    function getWheelsInfo() public view returns (WheelsInfo memory) {
        return wheelsInfo;
    }

    function getExtras() public view returns (Extra[] memory) {
        return extras;
    }
    function getModificationHistory() public view returns (Modification[] memory) {
       // modificationHistory.length;
        return modificationHistory;
    }

    function getEventHistory() public view returns (CarEvent[] memory) {
        //eventHistory.length;
        return eventHistory;
    }

    function getTransferedState() public view returns (bool) {
        return isTransfered;
    }
    function getTransferChassis() public view returns (string memory) {
        return transfer;
    }
    /////////////////////////


    ///////////////adds
    function addModification(uint256 timestamp, uint64 _uid, Part _modificationEnum,string memory _details ) public {
        require(timestamp <= block.timestamp,"Can't make changes in the future");
        timestamp = timestamp == 0 ? block.timestamp : timestamp;
        modificationHistory.push(Modification(timestamp,_uid,_modificationEnum, _details));
    }

    function addEvent(uint256 timestamp, uint64 _uid,EventName _eventEnum,string memory _details ) public {
        require(timestamp <= block.timestamp,"Can't make changes in the future");
        timestamp = timestamp == 0 ? block.timestamp : timestamp;
        eventHistory.push(CarEvent(timestamp,_uid,_eventEnum, _details));
    }

    function addExtra(uint256 timestamp,uint64 _uid, string memory _details) public{
        addModification(timestamp,_uid, Part.Other,_details);
        //uint64 newId = extras.length > 0 ? extras[extras.length - 1].id + 1 : 0;
        extras.push(Extra( block.timestamp,_uid, _details));
    }

    function addTransfer(uint256 timestamp,uint64 _uid,string memory _value) public {
        require(!isTransfered, "This car is already transfered");
        addModification(timestamp,_uid, Part.Other,string(abi.encodePacked("Car transfered to  ",_value)));
        isTransfered=true;
        transfer=_value;
    }
    ///////////////////////////////////////////

    //////////////////////////schimbari componente
    function modifyKm(uint256 timestamp,uint64 _uid, uint32 _nokm) public {
        //require(currentCarInfo.noKm < _nokm, "You can't enter a lower number of km");
        addModification(timestamp, _uid, Part.Odometer , string(abi.encodePacked("Km changed from ",uint32ToString(currentCarInfo.noKm), " to ",uint32ToString(_nokm))));
        currentCarInfo.noKm=_nokm;
    }
    //nu cred ca se schimba caroseria
    function modifyBodyType(uint256 timestamp,uint64 _uid, string memory _body) public {
        addModification(timestamp,_uid, Part.Body , string(abi.encodePacked("Body Type changed from ",currentCarInfo.bodyType, " to ", _body)));
        currentCarInfo.bodyType=_body;
    }

    function modifyGearbox(uint256 timestamp,uint64 _uid, string memory _gearbox) public {
        addModification(timestamp,_uid, Part.Transmission , string(abi.encodePacked("Gearbox changed from ",currentCarInfo.gearbox, " to ", _gearbox)));
        currentCarInfo.gearbox=_gearbox;
    }
    function modifyColor(uint256 timestamp,uint64 _uid, string memory _color) public {
        addModification(timestamp,_uid, Part.Exterior , string(abi.encodePacked("Color changed from ",currentCarInfo.color, " to ", _color)));
        currentCarInfo.color=_color;
    }

    function modifyNoSeats(uint256 timestamp,uint64 _uid, uint32 _noSeats) public {
        addModification(timestamp,_uid, Part.Interior , string(abi.encodePacked("Num of seats changed from ",uint32ToString(currentCarInfo.noSeats), " to ", uint32ToString(_noSeats))));
        currentCarInfo.noSeats=_noSeats;
    }

    function modifyNoDoors(uint256 timestamp,uint64 _uid, uint32 _noDoors) public {
        addModification(timestamp,_uid, Part.Exterior , string(abi.encodePacked("Num of doors changed from ",uint32ToString(currentCarInfo.noDoors), " to ", uint32ToString(_noDoors))));
        currentCarInfo.noDoors=_noDoors;
    }

    function modifyTransmission(uint256 timestamp,uint64 _uid, string memory _transmission) public {
        addModification(timestamp,_uid, Part.Transmission , string(abi.encodePacked("Transmission changed from ",currentCarInfo.transmission, " to ", _transmission)));
        currentCarInfo.transmission=_transmission;
    }


    function modifyEngine(uint256 timestamp,uint64 _uid,string memory _serial, string memory _liters, uint32 _hp,string memory _fuelType) public {
        addModification(timestamp,_uid, Part.Engine , string(abi.encodePacked("Engine changed from ",engineInfo.serial , " to ", _serial, " with this details: ", _liters, " l, ", uint32ToString(_hp), " hp, ", _fuelType)));
        engineInfo.serial=_serial;
        engineInfo.liters=_liters;
        engineInfo.horsePower=_hp;
        engineInfo.fuelType=_fuelType;
    }

    function modifyWheels(uint256 timestamp,uint64 _uid,uint32 _noWheels,uint32  _diameter,uint32  _width) public {
        if( _diameter==0 || _width==0){
            revert("Invalid wheel sizes.");
        }
        if (_noWheels==0){
           _noWheels=wheelsInfo.noWheels;
        }
        addModification(timestamp,_uid, Part.Engine , string(abi.encodePacked("Wheels changed  to: ",uint32ToString(_noWheels), " wheels, ", uint32ToString(_diameter), " cm, ", uint32ToString(_width), " cm.")));
        wheelsInfo.noWheels=_noWheels;
        wheelsInfo.diameter=_diameter;
        wheelsInfo.width=_width;
    }

    ///////////////////////////
    


    function uint32ToString(uint32 number) public pure returns (string memory) {
        if (number == 0) {
            return "0";
        }
        
        uint32 temp = number;
        uint length;
        while (temp != 0) {
            length++;
            temp /= 10;
        }

        bytes memory buffer = new bytes(length);
        while (number != 0) {
            length -= 1;
            buffer[length] = bytes1(uint8(48 + (number % 10)));
            number /= 10;
        }

        return string(buffer);
    }


}


struct TotalInfo {
    GeneralInfo carInfo;
    Modification[] modificationHistory;
    CarEvent[] CarEventHistorys;
}

struct Modification {
    uint256 timestamp;
    uint64 userId;
    Part enumPart;
    string details;
}

struct CarEvent {
    uint256 timestamp;
    uint64 userId;
    EventName eventNum;
    string details;
}


struct GeneralInfo {
    string chassisNumber;//VF1RFE00461322340
    uint32 manufacturingYear;//2018
    string manufacturer;//Renault
    string model;//Kadjar
    //modificabile
    string bodyType;//caroserie: SUV
    string gearbox; //Manuala/automata/One_gear
    string color;//negru
    uint32 noSeats; //2
    uint32 noDoors; //4
    uint32 noKm;//100000
    string transmission; // tractiune fata/spate
}

struct EngineInfo{
    string serial;
    string liters;
    uint32 horsePower;
    string fuelType; // diesel/benzina/electric/hibrid
}


struct WheelsInfo{
    uint32 noWheels;
    uint32 diameter;
    uint32 width;
}

struct Extra{
     uint256 timestamp;
    uint64 userId;
    string details;
}

enum Part {
    Odometer,
    Engine,
    Transmission,
    Suspension,
    Brakes,
    Wheels,
    Body,
    Interior,
    Exterior,
    Electronics,
    Other
}

enum EventName {
    Crash,
    Theft,
    Damage,
    TechnicalRevision,
    ITP,
    Purchase,
    Sale,
    Service,
    Mentenance,
    Register,
    Other
}