import {Component, HostListener, OnInit} from '@angular/core';
import {Web3Service} from './shared/service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError, filter, fromEvent, map, of, Subject, Subscriber, Subscription} from "rxjs";
import {HttpService} from "./shared/http.service";
import {StorageService} from "./shared/storage.service";
import {NavigationEnd, Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']

})
export class AppComponent implements OnInit {
  title = 'frontend';
  showUser: boolean = false;
  showAdmin: boolean = false;
  showProfileButton:boolean=false;

  //todo gasit cum se face salvatul imaginii in ipfs
  constructor(private httpService: HttpService, private storageService: StorageService, private router: Router,private fb:FormBuilder) {
    // this.image = undefined;
    // const ipfs = require('ipfs-api')('localhost', '5001');
    //
    // const result =  ipfs.add(this.image);
    // this.ipfsHash = result[0].hash;

  }

  ngOnInit(): void {
  this.initializeSubscribes()
  }

  initializeSubscribes(){

    this.showUser = this.storageService.getUser();
    this.storageService.getUserObserver().subscribe(data => {
      this.showUser = data;
      console.log("User: ", data);
    })


    this.showAdmin=this.storageService.getAdmin()
    this.storageService.getAdminObserver().subscribe(data => {
      this.showAdmin = data;
      console.log("Admin: ", data);
    })



    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        switch (event.url) {
          case "/home":
          case "/info":
            this.showProfileButton= true;
            break;
          default:
            this.showProfileButton = false;
            break;
        }
      }
    });

  }

  //ipfsHash: string;

  redirectToProfile() {
    if (this.showUser) {
      this.router.navigate(['/user']);
    }
    if (this.showAdmin) {
      this.router.navigate(['/admin']);
    }
  }




  logout() {
    localStorage.removeItem('token');
    this.storageService.setAdmin(false);
    this.storageService.setUser(false);

    this.httpService.logout().subscribe(data=>{
      console.log(data)
    },console.log)

    this.router.navigate(['/home']);
  }

  goToHome(section:string){
    this.router.navigate(['/home']).then(() => {
      const element = document.getElementById(section);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });  }
}
