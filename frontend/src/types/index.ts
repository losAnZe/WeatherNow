export type Risk='LOW'|'MODERATE'|'HIGH'|'SEVERE';
export type EventType='Severe Thunderstorm'|'Cloudburst'|'Flash Flood';
export interface WeatherEvent {id:string;type:EventType;name:string;region:string;latitude:number;longitude:number;riskLevel:Risk;probability:number;confidence:number;forecastStart:number;forecastEnd:number;currentStatus:string;affectedArea:number;primaryTriggers:string[];indicators:Record<string,number>;dataSource:string}
export interface ForecastHour {hour:number;thunderstorm:number;cloudburst:number;flashFlood:number;rainfall:number;riskLevel:Risk}
export interface Alert {id:string;eventType:EventType;severity:string;location:string;probability:number;forecastWindow:string;message:string;generatedAt:string;status:string}
export interface Cell {id:string;lat:number;lng:number;thunderstorm:number;cloudburst:number;flashFlood:number;rainfall:number;iwv:number;cape:number;cin:number;cttChange:number;windSpeed:number;elevation:number;slope:number;drainage:number;terrainRisk:number}
