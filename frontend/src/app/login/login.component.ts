import {Component} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {HttpService} from "../shared/http.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm!: FormGroup;
  showLoginError: boolean = false;
  errorMessage: string = "Username and password are required!";

  constructor(private requests: HttpService, private fb: FormBuilder, private router: Router) {
  }


  ngOnInit(): void {
    this.loginForm = this.fb.group({
      /*usernameField: ['', Validators.required], // todo cand nu testez
      passwordField: ['', Validators.required]*/
      usernameField: [''],
      passwordField: ['']
    });
  }

  login(event: Event) {
    event.preventDefault()
    if (this.loginForm.valid) {
      this.showLoginError = false;
      let username = this.loginForm.value.usernameField
      let password = this.loginForm.value.passwordField

      if (username==="" && password ===""){ // todo de scos cand nu testez
        username = "user1";
        password = "parola";
      }
      //todo citit despre salt si hash https://www.troyhunt.com/our-password-hashing-has-no-clothes/
      // pt ca aparent nu mai e ok sa folosesti doar hash https://stackoverflow.com/questions/43893516/how-to-implement-sha-256-encryption-in-angular2

      this.requests.login({username: username, password: password}).subscribe(data => {
        console.log(data);
        let role = sessionStorage.getItem('role')
        if(role){
          if (role === "ADMIN"){
            this.router.navigate(['/admin']);
          }
          else if (role === "USER"){
            this.router.navigate(['/user']);
          }
        }

      }, error => {
        console.log(error);
        this.errorMessage = "Wrong credentials!";
        this.showLoginError = true;
      });


    } else {
      this.showLoginError = true;
    }
    //this.searchForm.reset();
  }

}
