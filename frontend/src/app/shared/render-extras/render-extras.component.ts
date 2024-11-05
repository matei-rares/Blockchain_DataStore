import {Component, Input} from '@angular/core';
import {DatePipe} from "@angular/common";
import {getEventNameByValue} from "../enums";

@Component({
  selector: 'app-render-extras',
  templateUrl: './render-extras.component.html',
  styleUrls: ['./render-extras.component.scss'],
  providers: [DatePipe]

})
export class RenderExtrasComponent {
  @Input() extras: any;
  constructor(protected datePipe:DatePipe){
  }
}
