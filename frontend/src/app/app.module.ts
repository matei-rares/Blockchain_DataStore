import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { InfoComponent } from './info/info.component';
import { UserComponent } from './user/user.component';
import { AdminComponent } from './admin/admin.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {Interceptor} from "./shared/interceptor.service";
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {CommonModule, NgOptimizedImage} from "@angular/common";
import { RenderCarComponent } from './shared/render-car/render-car.component';
import { RenderModificationsComponent } from './shared/render-modifications/render-modifications.component';
import { RenderEventsComponent } from './shared/render-events/render-events.component';
import { RenderExtrasComponent } from './shared/render-extras/render-extras.component';
import {StorageService} from "./shared/storage.service";
import { LogoutButtonComponent } from './shared/logout-button/logout-button.component';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    InfoComponent,
    UserComponent,
    AdminComponent,
    RenderCarComponent,
    RenderModificationsComponent,
    RenderEventsComponent,
    RenderExtrasComponent,
    LogoutButtonComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        ReactiveFormsModule,
        HttpClientModule,
        MatAutocompleteModule,
        MatInputModule,
        FormsModule,
        BrowserAnimationsModule,
        CommonModule,
        NgOptimizedImage,
      SweetAlert2Module
    ],
  providers: [{provide:HTTP_INTERCEPTORS,useClass:Interceptor,multi:true},StorageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
