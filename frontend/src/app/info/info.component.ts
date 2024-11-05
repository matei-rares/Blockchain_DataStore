import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {HttpService} from "../shared/http.service";
import {Subscription} from "rxjs";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.scss']
})
export class InfoComponent implements OnInit,OnDestroy {
  showErrorMessage: boolean = false;
  private queryParamsSubscription!: Subscription;
  searchForm!: FormGroup;
  showChassisError: boolean = false;
  titleVIN : string ="";

  constructor(private route: ActivatedRoute, private fb: FormBuilder, private router: Router, private requests: HttpService) {
  }

  ngOnInit() {
    console.log("init")
    this.queryParamsSubscription=this.route.queryParams.subscribe(params => {

      const receivedData = params['data'];
      if (receivedData) {
        //////initializare form
        this.searchForm = this.fb.group({
          chassisField: [receivedData, Validators.required]
        });
        this.titleVIN= receivedData;
        ////

        this.getCarinfo(receivedData);

      } else {
        console.log("No data received")
        this.router.navigate(['/home']);
      }
    });
  }


  ngOnDestroy() {
    if (this.queryParamsSubscription) {
      this.queryParamsSubscription.unsubscribe();
    }
  }

  carInfo:any;
  getCarinfo(chassis: string) {
    this.requests.getCarInfo(chassis).subscribe(data => {
        console.log(data)
        this.carInfo=data.data;
      },
      error => {
        console.log(error)
        if (error.status == 404) {
          console.log("Car not found")
        } else {
          console.log("Error: ", error)
        }
      })
  }
  errorMesage: string = "Chassis is required!";



  searchCar(event: Event) {
    event.preventDefault()
    if (this.searchForm.valid) {
      this.showChassisError = false;
      let chassis = this.searchForm.value.chassisField
      console.log('Searched chassis:', chassis);

      this.requests.getCarInfo(chassis).subscribe(data => {
        console.log(data)
        this.carInfo=data.data;
        this.titleVIN= chassis;
      }, error => {
        console.log(error);
        this.errorMesage = "There is no car with this chassis " ;
        this.showChassisError = true;
      })

    } else {
      if(this.searchForm.value.chassisField == ""){
        this.errorMesage = "Chassis is required!";
      }
      this.showChassisError = true;
    }
    //this.searchForm.reset();
  }


}
