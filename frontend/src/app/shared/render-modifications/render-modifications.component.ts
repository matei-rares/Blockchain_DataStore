import {Component, Input} from '@angular/core';
import {getPartNameByValue} from "../enums";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-render-modifications',
  templateUrl: './render-modifications.component.html',
  styleUrls: ['./render-modifications.component.scss'],
  providers: [DatePipe]

})
export class RenderModificationsComponent {
  @Input() modifications: any;
  constructor(protected datePipe:DatePipe){

  }
  protected readonly getPartNameByValue = getPartNameByValue;
}
