import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AppComponent} from "./app.component";
import {UserComponent} from "./user/user.component";
import {AdminComponent} from "./admin/admin.component";
import {HomeComponent} from "./home/home.component";
import {InfoComponent} from "./info/info.component";
import {LoginComponent} from "./login/login.component";
import {Guardian} from "./shared/guardian.service";

const routes: Routes = [
  {path: 'user', component: UserComponent, canActivate: [Guardian]},
  {path: 'admin', component: AdminComponent, canActivate: [Guardian]},
  {path: 'home', component: HomeComponent},
  {path: 'info', component: InfoComponent},
  {path: 'login', component: LoginComponent},
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: '**', redirectTo: 'home'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
