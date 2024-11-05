import { Injectable } from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable()
export class StorageService {

  private userSub= new Subject<boolean>();
  constructor() {
  }
  getUserObserver(): Observable<boolean> {
    return this.userSub.asObservable();
  }


  setUser(value:boolean) {
    sessionStorage.setItem('user', value.toString());
    this.userSub.next(value);
  }

  getUser() {
    return sessionStorage.getItem('user') === 'true';
  }



  private adminSub= new Subject<boolean>();
  getAdminObserver(): Observable<boolean> {
    return this.adminSub.asObservable();
  }
  setAdmin(value:boolean) {
    sessionStorage.setItem('admin', value.toString());
    this.adminSub.next(value);
  }

  getAdmin() {
    return sessionStorage.getItem('admin') === 'true';
  }


}
