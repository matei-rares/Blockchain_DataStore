import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot} from '@angular/router';
import {HttpService} from "./http.service";
import {catchError, map, Observable, of} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SessionGuardService implements CanActivate {
  constructor(private requests: HttpService) {
  }

  canActivate(): boolean {

    return true;
  }

}
