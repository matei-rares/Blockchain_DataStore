import {Component, OnInit} from '@angular/core';
import {Form, FormBuilder, FormControl, FormGroup, NgControl, Validators} from "@angular/forms";
import {HttpService} from "../shared/http.service";
import {map, Observable, startWith} from "rxjs";
import {Part, EventName, eventKeyNames, partKeyNames, getPartNameByValue, getEventNameByValue} from "../shared/enums";
import {DatePipe} from "@angular/common";
import {StorageService} from "../shared/storage.service";
import {Router} from "@angular/router";
import Swal, {SweetAlertIcon} from "sweetalert2";

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
  providers: [DatePipe]
})
export class UserComponent implements OnInit {

  mockCarInfo = {
    generalInfo: {
      chassisNumber: '123256780',
      manufacturingYear: 2023,
      manufacturer: 'Toyota',
      model: 'Camry',
      bodyType: 'Sedan',
      gearbox: 'Automatic',
      color: 'Red',
      noSeats: 5,
      noDoors: 4,
      noKm: 5000,
      transmission: 'FWD'
    },
    engineInfo: {
      serial: 'ABCDE12345',
      liters: 2.5.toString(),
      horsepower: 200,
      fuelType: 'Gasoline'
    },
    wheelsInfo: {
      noWheels: 4,
      diameter: 18,
      width: 225
    }
  };

  chassies: string[] = [];
  currentChassis = '';
  currentCarDetails!: any;

  searchControl = new FormControl();
  filteredOptions!: Observable<string[]>;
  showSuggestions = false;

  contentView = 'None';


  selectedEvent!: EventName;
  eventDetails = '';

  selectModification!: Part;
  modificationDetails = '';

  extraDetails = '';

  public addCarForm: FormGroup = this.fb.group({
    chassisNumber: new FormControl('', [Validators.required, Validators.minLength(5)]),
    bodyType: ['', Validators.required],
    color: ['', Validators.required],
    gearbox: ['', Validators.required],
    manufacturer: ['', Validators.required],
    manufacturingYear: ['', [Validators.required, Validators.min(1886), Validators.max(new Date().getFullYear())]],
    model: ['', Validators.required],
    noDoors: ['', [Validators.required, Validators.min(0)]],
    noKm: ['', [Validators.required, Validators.min(0)]],
    noSeats: ['', [Validators.required, Validators.min(0)]],
    transmission: ['', Validators.required],
    serial: ['', Validators.required],
    fuelType: ['', Validators.required],
    horsepower: ['', [Validators.required, Validators.min(0)]],
    liters: ['', [Validators.required, Validators.min(0)]],
    diameter: ['', [Validators.required, Validators.min(0)]],
    noWheels: ['', [Validators.required, Validators.min(0)]],
    width: ['', [Validators.required, Validators.min(0)]],
  });
  clickedAdd: any = false;
  protected readonly eventKeyNames = eventKeyNames;
  protected readonly getEventNameByValue = getEventNameByValue;
  protected readonly partKeyNames = partKeyNames;
  protected readonly getPartNameByValue = getPartNameByValue;
  protected readonly Object = Object;

  constructor(private router: Router, private storageService: StorageService, protected datePipe: DatePipe, private requests: HttpService, private fb: FormBuilder) {
    storageService.setUser(true)
    this.clickedAdd = false;
  };


  ngOnInit(): void {
    sessionStorage.setItem('sessionRedirect', 'false')
    this.getChassies()
    //this.initializeCarDetails('12345678')
    this.changeView("Modifications")
    this.clickedAdd = false;
  }

  changeView(view: string) {
    if (view !== 'Add') {
      this.clickedAdd = false;
    }
    this.contentView = view
  }

  getChassies() {
    this.requests.getAllChassies().subscribe(data => {
        console.log(data)
        this.chassies = Object.values(data.data)
        this.initializeOptions()
      },
      console.log)
  }

  initializeOptions() {
    this.filteredOptions = this.searchControl.valueChanges.pipe(
      startWith(''),
      map(value =>
        this.chassies.filter(option => option.toLowerCase().includes(value.toLowerCase())))
    );
  }

  initializeCarDetails(chassis: string) {
    this.requests.getCarInfo(chassis).subscribe(data => {
        console.log(data)
        this.currentChassis = chassis
        this.currentCarDetails = data.data
      },
      console.log)
  }

  selectOption(option: string): void {
    this.searchControl.setValue(option);
    this.showSuggestions = false;
  }

  chooseCar() {
    if (this.searchControl.value === '' || !this.chassies.includes(this.searchControl.value)) {
      console.log("This car doesn't exist")
      this.currentChassis = ''
      return
    }
    this.currentChassis = this.searchControl.value;
    this.requests.getCarInfo(this.currentChassis).subscribe(data => {
        console.log(data)
        this.currentCarDetails = data.data
        this.contentView = "Details"
      },
      console.log)

  }

  getErrorMessage() {
    if (this.anyRequiredFieldInvalid()) {
      return 'All fields are required';
    } else if (this.isManufacturingYearInvalid()) {
      return 'Manufacturing Year needs to be at least 1886 and at most the current year';
    } else if (this.anyMinConditionInvalid()) {
      return 'Some fields do not meet the minimum requirements';
    } else {
      return null;
    }
  }

  anyRequiredFieldInvalid() {
    return Object.keys(this.addCarForm.controls).some(control =>
      this.addCarForm.controls[control].hasError('required')
    );
  }

  isManufacturingYearInvalid() {
    const control: any = this.addCarForm.get('manufacturingYear');
    return control.hasError('min') || control.hasError('max');
  }

  anyMinConditionInvalid() {
    return Object.keys(this.addCarForm.controls).some(control =>
      this.addCarForm.controls[control].hasError('min') && !this.addCarForm.controls[control].hasError('required')
    );
  }


  addCar() {
    // manufacturingYear: [''],
    //   manufacturer: [''],
    //   model: [''],
    //   bodyType: [''],
    //   gearbox: [''],
    //   color: [''],
    //   noSeats: [''],
    //   noDoors: [''],
    //   noKm: [''],
    //   transmission: [''],
    //   serial: [''],
    //   liters: [''],
    //   horsepower: [''],
    //   fuelType: [''],
    //   noWheels: [''],
    //   diameter: [''],
    //   width: ['']
    //
    //
    // this.addCarForm.get('chassisNumber')!.setValue(this.currentChassis)
    this.clickedAdd = true;

    if (this.addCarForm.invalid) {
      console.log("Invalid form")
      return
    }

    Swal.fire({
      allowEnterKey: true,
      allowEscapeKey: true,
      title: 'Warning!',
      text: 'This action is permanent, make sure all the data is correct. Do you want to proceed ?',
      showDenyButton: true,
      confirmButtonText: 'Yes',
      denyButtonText: `No`,
      confirmButtonColor: "#4b9b63",
      denyButtonColor: "#d20c2e",
      background: '#fff2e9',
      animation: true,
    }).then((result) => {
      if (result.isConfirmed) {
        console.log("confirmed")
        this.requests.addCar(this.convertFormGroupToObject(this.addCarForm)).subscribe(
          data => {
            console.log(data)

            Swal.fire({
              position: "top-end",
              icon: "success",
              title: "Car added!",
              timer: 2000,
              showConfirmButton: false,
              width: 190,
              animation: true,
              toast: true,
            });
          }, console.log
        );
      } else if (result.isDenied) {
        console.log("denied")
        return
      }
    })


  }

  addEvent() {
    EventName[this.selectedEvent] // accesez valoare (this.selectedEvent e numele cheii)
    EventName[0] // accesez numele cheii

    this.requests.addEvent(this.currentChassis, {
      eventEnum: EventName[this.selectedEvent],
      details: this.eventDetails
    }).subscribe(
      data => {
        console.log(data)
      }, console.log
    );

  }

  addModification() {
    Part[this.selectModification] // accesez valoare (this.selectedEvent e numele cheii)
    Part[0] // accesez numele cheii

    this.requests.addModification(this.currentChassis, {
      partEnum: Part[this.selectModification],
      details: this.modificationDetails
    }).subscribe(
      data => {
        console.log(data)
      }, console.log
    );

  }

  addExtra() {

    this.requests.addExtra(this.currentChassis, {details: this.extraDetails}).subscribe(
      data => {
        console.log(data)
      }, console.log
    );

  }

  convertFormGroupToObject(formGroup: FormGroup) {
    const generalInfo = formGroup.getRawValue();
    const engineInfo = {
      serial: formGroup.get('serial')!.value,
      liters: formGroup.get('liters')!.value.toString(),
      horsepower: formGroup.get('horsepower')!.value,
      fuelType: formGroup.get('fuelType')!.value
    };
    const wheelsInfo = {
      noWheels: formGroup.get('noWheels')!.value,
      diameter: formGroup.get('diameter')!.value,
      width: formGroup.get('width')!.value
    };

    return {
      generalInfo,
      engineInfo,
      wheelsInfo
    };
  }

  // onSubmit() {
  //   const carInfo = this.convertFormGroupToObject(this.addCarForm);
  //   console.log(carInfo);
  // }

  modifyKm() {
    let km: number = +(<HTMLInputElement>document.getElementById('km_input')).value
    if (isNaN(km)) {
      console.log("Invalid km")
      this.fireSwalError("error", "Please enter a valid number")
      return
    } else if (km < 0) {
      this.fireSwalError("error", "Number must be greater than 0 ")
      return
    }
    this.requests.modifyKm(this.currentChassis, {km: km}).subscribe(data => {
      console.log(data)
    }, console.log)
  }


  modifyColor() {
    let color: string = (<HTMLInputElement>document.getElementById('color_input')).value
    if (color === '') {
      console.log("Invalid color")
      this.fireSwalError("error", "Please enter a valid color")
      return
    }
    this.requests.modifyColor(this.currentChassis, {color: color}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyTranfer() {
    let transfer: string = (<HTMLInputElement>document.getElementById('transfer_input')).value

    if ( this.currentCarDetails.transfer !== "") {
      console.log("Car already has a transfer")
      this.fireSwalError("error", "Car already has a transfer")
      return
    } else if (transfer === '' ) {
      console.log("Invalid transfer")
      this.fireSwalError("error", "Please enter a valid transfer")
      return
    }


    this.requests.addTransfer(this.currentChassis, {transfer: transfer}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyNoseats() {
    let no_seats: number = +(<HTMLInputElement>document.getElementById('nos_input')).value
    if (isNaN(no_seats)) {
      console.log("Invalid no seats")
      this.fireSwalError("error", "Please enter a valid number")
      return
    } else if (no_seats < 0) {
      this.fireSwalError("error", "Number must be greater than 0 ")
      return
    }
    this.requests.modifyNoseats(this.currentChassis, {no_seats: no_seats}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyNodoors() {
    let no_doors: number = +(<HTMLInputElement>document.getElementById('nod_input')).value
    if (isNaN(no_doors)) {
      console.log("Invalid no seats")
      this.fireSwalError("error", "Please enter a valid number")
      return
    } else if (no_doors < 0) {
      this.fireSwalError("error", "Number must be greater than 0 ")
      return
    }
    this.requests.modifyNodoors(this.currentChassis, {no_doors: no_doors}).subscribe(data => {
      console.log(data)
    }, console.log)
  }


  modifyTransmission() {
    let transmission: string = (<HTMLInputElement>document.getElementById('trans_input')).value
    if (transmission === '') {
      console.log("Invalid transmission")
      this.fireSwalError("error", "Please enter a valid transmission")
      return
    }
    this.requests.modifyTransmission(this.currentChassis, {transmission: transmission}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyGearbox() {
    let gearbox: string = (<HTMLInputElement>document.getElementById('gear_input')).value
    if (gearbox === '') {
      console.log("Invalid gearbox")
      this.fireSwalError("error", "Please enter a valid gearbox")
      return
    }
    this.requests.modifyGearbox(this.currentChassis, {gearbox: gearbox}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyEngine() {
    let serial: string = (<HTMLInputElement>document.getElementById('es_input')).value
    let liters: number = +(<HTMLInputElement>document.getElementById('el_input')).value
    let horsepower: number = +(<HTMLInputElement>document.getElementById('eh_input')).value
    let fuel: string = (<HTMLInputElement>document.getElementById('ef_input')).value

    if (serial === '' || fuel === '') {
      console.log("Invalid fields")
      this.fireSwalError("error", "Please enter a valid engine")
      return
    } else if (horsepower < 0 || liters < 0) {
      this.fireSwalError("error", "Numbers must be greater than 0 ")
    }

    this.requests.modifyEngine(this.currentChassis, {serial: serial, liters:liters,horsepower:horsepower,fuel_type:fuel}).subscribe(data => {
      console.log(data)
    }, console.log)
  }

  modifyWheels() {
    let no_wheels: number = +(<HTMLInputElement>document.getElementById('wn_input')).value
    let diameter: number = +(<HTMLInputElement>document.getElementById('wd_input')).value
    let width: number = +(<HTMLInputElement>document.getElementById('ww_input')).value


    if (no_wheels < 0 || diameter< 0 || width < 0 ) {
      console.log("Invalid wheels")
      this.fireSwalError("error", "Please enter numbers greater than 0")
      return
    }
    this.requests.modifyWheels(this.currentChassis, {no_wheels: no_wheels,diameter:diameter,width:width}).subscribe(data => {
      console.log(data)
    }, console.log)
  }


  fireSwalError(icon: undefined | SweetAlertIcon, text: string) {
    Swal.fire({
      icon: icon,
      // title: title,
      text: text,
      // confirmButtonColor: "#4b9b63",
      // background: '#fff2e9',
      animation: true,
      position: "top-end",
      timer: 2000,
      showConfirmButton: false,
      width: 250,
      toast: true,
    })
  }


}
