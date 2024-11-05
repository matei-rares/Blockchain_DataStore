import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class Interceptor implements HttpInterceptor {
  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      tap(event => {
        if (event instanceof HttpResponse) {
          const newTokenHeader = event.headers.get('X-New-Token');
          if (newTokenHeader) {
            localStorage.setItem('token', newTokenHeader);
          }
          const role = event.headers.get('X-Role');
          if (role) {
            sessionStorage.setItem('role', role);
          }
        }
      })
    );
  }
}
