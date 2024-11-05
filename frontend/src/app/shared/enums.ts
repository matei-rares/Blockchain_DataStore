
export enum Part {
  Odometer,
  Engine,
  Transmission,
  Suspension,
  Brakes,
  Wheels,
  Body,
  Interior,
  Exterior,
  Electronics,
  Other
}
export enum EventName {
  Crash,
  Theft,
  Damage,
  TechnicalRevision,
  ITP,
  Purchase,
  Sale,
  Service,
  Mentenance,
  Register,
  Other
}
export const eventData = Object.keys(EventName) as (keyof typeof EventName)[];
export const eventKeyNames = eventData.filter(key => !isNaN(Number(EventName[key])));
export function getEventNameByValue( enumValue: number) {
  if (enumValue in EventName)
    return EventName[enumValue];
  return undefined;
}


export const partData = Object.keys(Part) as (keyof typeof Part)[];
export const partKeyNames = partData.filter(key => !isNaN(Number(Part[key])));
export function getPartNameByValue( enumValue: number) {
  if (enumValue in Part)
    return Part[enumValue];
  return undefined;
}

