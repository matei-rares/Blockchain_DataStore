import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {HttpService} from "../shared/http.service";
import {Router} from "@angular/router";
import {catchError, map, of} from "rxjs";
import Swal from "sweetalert2";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  searchForm: FormGroup = this.fb.group({
    chassisField: ['', Validators.required]
  });

  registerForm: FormGroup = this.fb.group({
    emailField: ['', [Validators.required, Validators.email]],
    nameField: ['', [Validators.required]],
    textField: ['',[Validators.required]]
  });

  showChassisError: boolean = false;
  errorMessage: string = "Chassis is required!";
  //constructor(private web3Service: Web3Service,private fb: FormBuilder) {}
  //this.web3Service.startService();
  constructor(private requests: HttpService, private fb: FormBuilder, private router: Router) {
    this.open_redirect()
  }




  getErrorMessage() {
    if (this.anyRequiredFieldInvalid()) {
      return 'All fields are required';
    } else if (this.isEmailValid()) {
      return 'Invalid email';
    }else {
      return null;
    }
  }
  anyRequiredFieldInvalid() {
    return Object.keys(this.registerForm.controls).some(control =>
      this.registerForm.controls[control].hasError('required')
    );
  }

  isEmailValid() {
    const control:any = this.registerForm.get('emailField');
    return control.hasError('email') ;
  }


  ngOnInit(): void {

  }

  searchCar(event: Event) {
    event.preventDefault()
    if (this.searchForm.valid) {
      this.showChassisError = false;
      let chassis = this.searchForm.value.chassisField
      console.log('Searched chassis:', chassis);

      this.requests.checkExistence(chassis).subscribe(data => {
        this.router.navigate(['/info'], {queryParams: {data: chassis}});
      }, error => {
        console.log(error);
        this.errorMessage = "There is no car with this chassis ";
        this.showChassisError = true;
      })

    } else {

      if (this.searchForm.value.chassisField == "") {
        this.errorMessage = "Chassis is required!";
      }
      this.showChassisError = true;
    }
    //this.searchForm.reset();
  }

  open_redirect() {
    let tok = localStorage.getItem('token')
    var auth: boolean = tok != null && true && tok != ""

    // daca nu  a ajuns pe user sau admin va fi redirectionat acolo
    // daca exista token, daca nu merge la home

    if (auth) {
      let redirectUser= sessionStorage.getItem('sessionRedirect') === null
      if (!redirectUser) {
        return
      }



      //daca tokenu nu mai e valid merge la login
      this.requests.refresh().subscribe(data => {

          const role = sessionStorage.getItem('role')
          if (role) {
            if (role === "ADMIN") {
              this.router.navigate(['/admin']);
            } else if (role === "USER") {
              this.router.navigate(['/user']);
            }
            return
          }
          this.router.navigate(['/login']);
        },
        error => {
          console.log(error);
          localStorage.removeItem('token');
          this.router.navigate(['/login']);

        }
      );
    }
  }

  goToSearch(){
    const element = document.getElementById("searchGo");
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  sendRegistration(event:FormDataEvent){
    event.preventDefault()
    console.log("Registration sent")
    console.log(this.registerForm.value)

    if (this.registerForm.invalid) {




      console.log("Invalid form")
      Swal.fire({
        position: "top-end",
        icon: "error",
        title: this.getErrorMessage()!,
        timer: 2000,
        showConfirmButton: false,
        width: 250,
        animation: true,
        toast: true,
      });
      return
    }

    this.requests.register(this.registerForm.value).subscribe(data=>{
      console.log(data)
      Swal.fire({
        position: "top-end",
        icon: "success",
        title: "Message sent!",
        timer: 2000,
        showConfirmButton: false,
        width: 190,
        animation: true,
        toast: true,
      });
    },console.log)
  }

}
