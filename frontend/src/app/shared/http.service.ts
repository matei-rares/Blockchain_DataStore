
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private http:HttpClient) {}

  backendURL:string = 'http://localhost:5000';
  getCarInfo(chassis:String){
    return this.http.get<any>(`${this.backendURL}/cars/car?chassis=${chassis}`)
  }

  checkExistence(chassis:String){
    return this.http.get<any>(`${this.backendURL}/cars/chassies?chassis=${chassis}`)
  }

  getAllChassies(){
    return this.http.get<any>(`${this.backendURL}/registry/chassies`, {headers: this.getAuthModifHeaders()} )
  }

  addCar(body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/cars`, body, {headers: this.getAuthModifHeaders()})
  }

  addEvent(chassis:string,body:any) {
    return this.http.post<any>(`${this.backendURL}/registry/${chassis}/events`, body, {headers: this.getAuthModifHeaders()})
  }

  addModification(chassis:string,body:any) {
    return this.http.post<any>(`${this.backendURL}/registry/${chassis}/modifications`, body, {headers: this.getAuthModifHeaders()})
  }


  addExtra(chassis:string,body:any) {
    return this.http.post<any>(`${this.backendURL}/registry/${chassis}/extras`, body, {headers: this.getAuthModifHeaders()})
  }

  addTransfer(chassis:string,body:any) {
    return this.http.post<any>(`${this.backendURL}/registry/${chassis}/transfer`, body, {headers: this.getAuthModifHeaders()})
  }

  modifyKm(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/km`, body, {headers: this.getAuthModifHeaders()})
  }

  modifyGearbox(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/gearbox`, body, {headers: this.getAuthModifHeaders()})
  }
  modifyColor(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/color`, body, {headers: this.getAuthModifHeaders()})
  }

  modifyNoseats(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/no_seats`, body, {headers: this.getAuthModifHeaders()})
  }
  modifyNodoors(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/no_doors`, body, {headers: this.getAuthModifHeaders()})
  }
  modifyTransmission(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/general/transmission`, body, {headers: this.getAuthModifHeaders()})
  }
  modifyEngine(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/engine`, body, {headers: this.getAuthModifHeaders()})
  }
  modifyWheels(chassis:string,body:any) {
    return this.http.put<any>(`${this.backendURL}/registry/${chassis}/wheels`, body, {headers: this.getAuthModifHeaders()})
  }

  login(body:any) {
    return this.http.post<any>(`${this.backendURL}/login`, body )
  }

  logout() {
    return this.http.post<any>(`${this.backendURL}/logout`, {},{headers:this.getAuthModifHeaders()} )
  }

  refresh(){
    return this.http.post<any>(`${this.backendURL}/refresh`, {}, {headers: this.getAuthModifHeaders()})
  }

  register(data:any){
    return this.http.post<any>(`${this.backendURL}/register`, data)
  }

  getAuthModifHeaders(){
    return  new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+localStorage.getItem('token')
    });
  }

  getUsers(){
    return this.http.get<any>(`${this.backendURL}/users`, {headers: this.getAuthModifHeaders()})
  }

  createUser(data:any){
    return this.http.put<any>(`${this.backendURL}/users/user`, data, {headers: this.getAuthModifHeaders()})


  }

  changeUserStatus(id:string,data:any){
    return this.http.put<any>(`${this.backendURL}/users/${id}/status`, data, {headers: this.getAuthModifHeaders()})
  }
}
