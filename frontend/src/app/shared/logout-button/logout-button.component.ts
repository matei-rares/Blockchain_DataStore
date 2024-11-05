import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {StorageService} from "../storage.service";
import {HttpService} from "../http.service";

@Component({
  selector: 'app-logout-button',
  templateUrl: './logout-button.component.html',
  styleUrls: ['./logout-button.component.scss']
})
export class LogoutButtonComponent {

  constructor(private httpService:HttpService,private router:Router, private storageService:StorageService) {}


  logout() {
    localStorage.removeItem('token');
    this.storageService.setAdmin(false);
    this.storageService.setUser(false);

    this.httpService.logout().subscribe(data=>{
      console.log(data)
    },console.log)

    this.router.navigate(['/home']);
  }
}
