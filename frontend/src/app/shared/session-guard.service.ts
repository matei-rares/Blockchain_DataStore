import {Injectable} from '@angular/core';
import { CanActivate} from '@angular/router';
import {HttpService} from "./http.service";

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
