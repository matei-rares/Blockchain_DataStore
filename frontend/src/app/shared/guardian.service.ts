import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot} from '@angular/router';
import {HttpService} from "./http.service";
import {catchError, map, Observable, of} from "rxjs";
import {StorageService} from "./storage.service";

@Injectable({
  providedIn: 'root'
})
export class Guardian implements CanActivate {
  constructor(private storageService:StorageService,private requests: HttpService, private router: Router) {
  }

  canActivate(next: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean | Observable<boolean> {
    let tok = localStorage.getItem('token')
    var auth: boolean = tok != null && true && tok != ""

    // daca exista token, daca nu merge la home
    if (auth) {
      //daca tokenu nu mai e valid merge la login
      return this.requests.refresh().pipe(
        map(response => {
          const role = sessionStorage.getItem('role')
          if (role) {
            if (role === "ADMIN" && state.url === "/admin" || state.url === "/user" && role === "USER") {
              return true;
            }
          }
          this.router.navigate(['/login']);
          return false;
        }),
        catchError(error => {
            console.log(error);
            localStorage.removeItem('token');
            this.storageService.setUser(false);
          this.storageService.setAdmin(false);
            this.router.navigate(['/login']);
            return of(false);
          }
        ));

    } else {
      this.router.navigate(['/home']);
      return false;
    }
  }

}
