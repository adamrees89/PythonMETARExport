# import metar
import requests
import psychrolib

psychrolib.SetUnitSystem(psychrolib.SI)

Airports = {
    "EGFF": "Cardiff",
    "EGGD": "Bristol",
    "EGSY": "MOD St Athan",
}

def METARGet(airport_code):
    baseURL = "https://aviationweather.gov/api/data/metar"
    params = {"ids": airport_code,
              "format" : "json"}
    
    response = requests.get(baseURL,params)
    data = response.json()
    
    return data

def PsychroCalc(METAROut):
    """
    This function calculates the psychrometric properties of air given the dry bulb temperature, dew point, and atmospheric pressure.
    It exposes the following and outputs them in a dictionary (AirCondition):
    - Temperature (C) - DBTemp
    - Dew Point (C) - DewPoint
    - Humidity Ratio (kg/kg) - HRatio
    - Wet Bulb Temperature (C) - WBTemp
    - Relative Humidity (%) - RHum
    - Vapour Pressure (Pa) - VPress
    - Enthalpy (kJ/kg) - Enthalpy
    - Specific Volume (m^3/kg) - SpVolume
    - Degree of Saturation (0-1) - Sat
    """
    DBTemp = METAROut[0]["temp"]
    DewPoint = METAROut[0]["dewp"]
    AtmosphericPressure = (METAROut[0]["altim"]+METAROut[0]["elev"]) *100
    
    # print(f"Input Data: Dry Bulb Temp: {DBTemp}°C, Dew Point Temp: {DewPoint}°C, Atmospheric Pressure: {AtmosphericPressure}Pa")
    
    Condition = psychrolib.CalcPsychrometricsFromTDewPoint(
        DBTemp,
        DewPoint,
        AtmosphericPressure)         
      
    AirCondition = {
        "DBTemp": DBTemp,
        "DewPoint": DewPoint,
        "AtmosphericPressure": AtmosphericPressure,
        "HRatio": Condition[0],
        "WBTemp": Condition[1],
        "RHum": Condition[2],
        "VPress": Condition[3],
        "Enthalpy": Condition[4],
        "SpVolume": Condition[5],
        "Sat": Condition[6]}
    
    return AirCondition

def PrintAirCondition(AirCondition,Airports,data):
        print(f"""
          Data Received for {Airports[data[0]['icaoId']]} ({data[0]['icaoId']})
          Psychrometric Properties:
          - Dry Bulb Temperature: {AirCondition['DBTemp']}°C
          - Dew Point Temperature: {AirCondition['DewPoint']}°C
          - Humidity Ratio: {AirCondition['HRatio']:.4f} kg/kg
          - Wet Bulb Temperature: {AirCondition['WBTemp']:.0f}°C
          - Relative Humidity: {AirCondition['RHum']:.0%}
          - Vapour Pressure: {AirCondition['VPress']:,.2f} Pa
          - Enthalpy: {AirCondition['Enthalpy']:,.2f} kJ/kg
          - Specific Volume: {AirCondition['SpVolume']:.4f} m³/kg
          - Degree of Saturation: {AirCondition['Sat']:.2f}
          """)

if __name__ == "__main__":
    
    for airport_code in Airports.keys():
        data = METARGet(airport_code)
        AirCondition = PsychroCalc(data)
        PrintAirCondition(AirCondition,Airports,data)