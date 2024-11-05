import {Component, Input} from '@angular/core';
import {getPartNameByValue} from "../enums";

@Component({
  selector: 'app-render-car',
  templateUrl: './render-car.component.html',
  styleUrls: ['./render-car.component.scss']
})
export class RenderCarComponent {
  @Input() car: any;

  get generalInfo(){
    return this.car.carInfo;
  }
  get engineInfo(){
    return this.car.engineInfo;
  }
  get eventHistory(){
    return this.car.eventHistory;
  }

  get extra(){
    return this.car.extra;
  }

  get modificationHistory(){
    return this.car.modificationHistory;
  }

  get wheelsInfo(){
    return this.car.wheelsInfo;
  }
  get generalInfoKeys(){
    return Object.keys(this.car.carInfo);
  }
  get engineInfoKeys() {
    return Object.keys(this.car.engineInfo);
  }

  get wheelsInfoKeys() {
    return Object.keys(this.car.wheelsInfo);
  }

  get analisis_ky(){
    return this.car.analisis.km_years;
  }
  get analisis_cds(){
    return this.car.analisis.crash_dam_ser;
  }
  get analisis_ms(){
    return this.car.analisis.men_sel;
  }

  get transfer(){
    return this.car.transfer;
  }

  get reversedOdometer(){
    return this.car.reversedOdometer;
  }

   addSpaceBeforeCapital(str:any ) {
     let modifiedStr = str.replace(/([A-Z])/g, ' $1');


     return modifiedStr.toLowerCase().replace(/^\w/, (c: string) => c.toUpperCase());
  }

  getStatusColor(value: number): string {
    if (value < 0.5) {
      return 'green';
    } else if (value >= 0.5 && value < 0.7) {
      return 'orange';
    } else if (value >= 0.7) {
      return 'red';
    } else {
      return 'gray';
    }
  }

  getTextByValue(value: number): string {
    if (value < 0.5) {
      return "It is unlikely that ";//"ca km sa fie dati inapoi" the mileage has been rolled back
    } else if (value >= 0.5 && value < 0.7) {
      return 'There is a low chance that ';
    } else if (value >= 0.7) {
      return 'There is a high chance that';
    } else {
      return 'Value error';
    }
  }

  getBiggestValue(value1:number,value2:number): number {
    return value1 > value2 ? value1 : value2;
  }


  protected readonly getPartNameByValue = getPartNameByValue;
}
