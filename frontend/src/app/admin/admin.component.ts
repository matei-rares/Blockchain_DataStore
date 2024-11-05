import {Component, OnInit} from '@angular/core';
import {StorageService} from "../shared/storage.service";
import {Event, Router} from "@angular/router";
import Swal from 'sweetalert2';
import {DatePipe} from "@angular/common";
import {HttpService} from "../shared/http.service";
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements  OnInit{

  users:any;
  createUserForm = this.fb.group({
    name: ['',[Validators.required]],
    username: ['',[Validators.required]],
    password: ['',[Validators.required]],
    company: ['',[Validators.required]],
  })
  constructor(private router: Router, private storageService: StorageService, private fb: FormBuilder,  private requests: HttpService) {
    storageService.setAdmin(true);
  }

  ngOnInit():void {
    sessionStorage.setItem('sessionRedirect', 'false')
    this.initializeUsers()
  }

  initializeUsers(){
    this.requests.getUsers().subscribe(data => {
        console.log(data)
        this.users = Object.values(data.data)

      },
      console.log)
  }

  createUser(event:any){
    event.preventDefault()
    if(this.createUserForm.valid){
      this.requests.createUser(this.createUserForm.value).subscribe(data => {
          console.log(data)
          this.initializeUsers()
        },
        console.log)
    }
    else{
      Swal.fire({
        position: "top-end",
        icon: "error",
        title: "All fields are required",
        timer: 2000,
        showConfirmButton: false,
        width: 250,
        animation: true,
        toast: true,
      });
    }

  }


  changeStatus(event:any,user:any) {
    event.preventDefault()

     let action=user.is_active == 0 ? "activate" : "deactivate"
    Swal.fire({
      allowEnterKey:true,
      allowEscapeKey:true,
      title: 'Hi there! ',
      text: 'Are you sure you want to '+action+' this user?',
      showDenyButton: true,
      confirmButtonText: 'Yes',
      denyButtonText: `No`,
      confirmButtonColor:"#356f48",
      denyButtonColor:"#a83246",
      width: 350,
      background: '#fff2e9',
      animation: true,
    }).then((result) => {
      if (result.isConfirmed) {
        console.log("confirmed")
        let status = user.is_active == 0 ? 1 : 0
        this.requests.changeUserStatus(user.id,{status:status}).subscribe(data => {
            console.log(data)
            this.initializeUsers()
          },
          console.log)
        return
      } else if (result.isDenied) {
        console.log("denied")
        return
      }
    })
  }
  currUser: any = null;
  selectedRow: number = -1;
  onRowClick(event: MouseEvent, user: any, index: number): void {
    this.currUser = user
    this.selectedRow = index;
    event.stopPropagation()
  }
}
