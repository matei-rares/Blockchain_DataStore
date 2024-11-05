import {Component, Input, OnInit} from '@angular/core';
import {DatePipe} from "@angular/common";
import {getEventNameByValue} from "../enums";

@Component({
  selector: 'app-render-events',
  templateUrl: './render-events.component.html',
  styleUrls: ['./render-events.component.scss'],
  providers: [DatePipe]

})
export class RenderEventsComponent{
  @Input() eventHistory: any;
  constructor(protected datePipe:DatePipe){
  }

  protected readonly getEventNameByValue = getEventNameByValue;


}
