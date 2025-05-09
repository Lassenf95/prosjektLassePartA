import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from smarthouse.persistence import SmartHouseRepository
from smarthouse.domain import SmartHouse, Room, Floor, Device, Sensor, Actuator, MIXActuatorSensor, Measurement 
from pathlib import Path
from typing import Union
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os
def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

##### pydantic modeller for forespørsler og respons validering
class ActuatorStateUpdate(BaseModel):
    stateNewValid: int

class MeasurementCreate(BaseModel):
    newValue: float #måleverdi
    newSensorUnit : str 
    newTimestamp: Optional[str] = None #optional, is not provided set ts as current time

class DeviceResponse(BaseModel):
    room_name: str
    id: str
    supplier: str
    model_name: str
    device_type: str

class MeasurementResponse(BaseModel):
    deviceId: str
    tidspunkt: str
    value: float
    unit: str

class ErrorResponse(BaseModel):
    error: str
    

class RoomResponse(BaseModel):
    room_name:str
    room_size: float
    room_id: int
    room_devices: list[dict[str,Union[str,float]]]
                       
class FloorResponse(BaseModel):
    floor_level:int
    rooms: list[str]                    
                       
                       
#####
if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }

# TODO: implement the remaining HTTP endpoints as requested in
# https://github.com/selabhvl/ing301-projectpartC-startcode?tab=readme-ov-file#oppgavebeskrivelse
# here ...

@app.get("/smarthouse/floor")
def get_floors() -> dict[str, list[dict[str, Union[int, list[str]]]]]:
    """
    This endpoint returns an object that provides information
    about all the floor in the smarthouse.
    """
    floors = smarthouse.get_floors() # henter ut alle etasjene

    #lager en liste for alle etasjene med info
    floor_info = []
    
    #henter ut info om hver etasje
    for floor in floors:
        info ={          
            "level": floor.level,
            "rooms": [room.room_name for room in floor.rooms]
        }
        floor_info.append(info)
    return {"floors": floor_info}


@app.get("/smarthouse/floor/{fid}")
def get_floor_info(fid: int):#-> dict: #[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about the given floor in the smarthouse.
    """
    floors = smarthouse.get_floors()  # Henter ut alle etasjene
    # Gå gjennom etasjene for å finne den spesifikke etasje
    for floor in floors:
        if floor.level == fid:  # Sammenlign med ==
            floor_info =FloorResponse (
                floor_level= floor.level,
                rooms= [room.room_name for room in floor.rooms]  # Liste over romnavn
            )
            return {'floor info': floor_info}
    # Hvis etasje ikke finnes, returner en feilmelding
    return ErrorResponse(error=f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen.")
    
@app.get("/smarthouse/floor/{fid}/room") 
def get_rooms_on_floor(fid: int) -> Union[list[RoomResponse], ErrorResponse]: 
    """
    This endpoint returns an object that provides information
    about all the rooms in the given floor in the smarthouse.
    """
    result=[]
    floors = smarthouse.get_floors()  # Get all the floors
    for floor in floors:
        if floor.level == fid:
            for rooms in floor.rooms:
                    roomRespo= RoomResponse(
                        room_name= rooms.room_name,
                        room_size= rooms.size,
                        room_id= rooms.id,
                        room_devices= [
                        {
                            'id': device.id,
                            'supplier': device.supplier,
                            'model_name': device.model_name,
                            'device type': device.device_type
                        } for device in rooms.devices
                        ]
                    )
                    result.append(roomRespo)
        return result                  
    # If the floor does not exist, return an error response
    return ErrorResponse(error=f"FFFloor with level {fid} does not exist in the smarthouse, please try another.")

@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_room_byID_onfloor(fid: int, rid: int): #-> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns ann object that provides information
    about the given rooms in the given floor in the smarthouse.
    """
    room_info = []
    floors = smarthouse.get_floors()  # Get all the floor
    for floor in floors:
        if floor.level == fid:
            for rooms in floor.rooms:
                if rooms.id == rid:
                    return RoomResponse(
                        room_name= rooms.room_name,
                        room_size= rooms.size,
                        room_id= rooms.id,
                        room_devices= [
                        {
                            'id': device.id,
                            'supplier': device.supplier,
                            'model_name': device.model_name,
                            'device type': device.device_type
                        } for device in rooms.devices
                        ]
                    )
    return ErrorResponse(error=f"Rom id {rid} finnes ikke i level {fid}, prøv noe annet.")
        
                       
    # #Hvis etasje ikke finnes, returner en feilmelding
    # return {
    #      "error": f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen."
    #  }
    

@app.get("/smarthouse/device")
def get_devices():# -> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about all the devices in the smarthouse
    """
    devices = smarthouse.get_devices()  # Get all devices in the smarthouse    
    result= []
    for device in devices:
        info =DeviceResponse(   
                room_name= device.room_name, #her er rommet til enheten
                id= device.id,
                supplier= device.supplier, 
                model_name= device.model_name,
                device_type= device.device_type
                )
        result.append(info)
    return result

    
@app.get("/smarthouse/device/{uuid}")
def get_device_by_id(uuid: str):# -> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about the device with uuid = device.id
    """
    device = smarthouse.get_device_by_id(uuid)  # Get all devices in the smarthouse    
    if device is None:
        return ErrorResponse(error=f"Device with id {uuid} was not found.")        
    return DeviceResponse (   
        room_name= device.room_name, #her er rommet til enheten
        id=  device.id,
        supplier= device.supplier, 
        model_name= device.model_name,
        device_type= device.device_type
        )
    
# @app.get("/smarthouse/device/{uuid}/current")
# def get_measurement_by_device_id(uuid: str) ->  Union[MeasurementResponse, ErrorResponse]: 
#     """
#     This endpoint returns the latest measurement for a device with the given UUID.
#     """
#     sensor = smarthouse.get_device_by_id(uuid) 
#     if sensor is None:
#         return ErrorResponse(error= f"Device with UUID {uuid} not found.")
#     if isinstance(sensor, Sensor) is False:
#         return  ErrorResponse(error=f"Device with UUID {uuid} is not an sensor, meausrement can't be read.")
#     measure = repo.get_latest_reading(sensor)
#     # MERK dette under blir er erstattet av Pydantic model(basemodel i toppen)
#     # return {
#     #     'timestamp': measure.timestamp,
#     #     'value': measure.value,
#     #     'unit': measure.unit
#     #     }
#     if measure is None:
#         return ErrorResponse(error="No measurements found for this sensor.")

#     return MeasurementResponse(deviceId=uuid,tidspunkt=measure[0],value=measure[1],unit=measure[2])       

@app.get("/smarthouse/device/{uuid}/current")
def get_measurement_by_device_id(uuid: str): # -> dict[str, Union[str, int]]:
    """
    This endpoint returns the latest measurement for the specified device.
    """
    device = smarthouse.get_device_by_id(uuid)  # Get all devices in the smarthouse    
    if device is None:
        return ErrorResponse(error=f"Device with id {uuid} was not found.")   
    # Check if the device is a Sensor
    if isinstance(device, Sensor):
        
        measure = repo.get_latest_reading(uuid)  # Pass the device as a Sensor
        if measure is not None:
            return MeasurementResponse(
                deviceId= uuid, #uses uuid as Measure does onlu contain ts value and unit
                tidspunkt= measure.timestamp,
                value= measure.value,
                unit= measure.unit
            )
    return ErrorResponse(error=f"The specified device is not a sensor.")

@app.post("/smarthouse/device/{uuid}/current")
def post_measurement_by_device_id(uuid: str, measurement : MeasurementCreate): 
    """
    This endpoint adds a measurement device(sensor) with the given UUID.
    Format on sesnor tabel is [device(key),ts,value,unit]
    So by using key a new value is to be given.
    as unit should not be dealt with, the same units from the device has to be reused.
    ts and value is free to choose - TODO secure format
    """
    sensor = smarthouse.get_device_by_id(uuid) 
    if sensor is None:
        return {"error": f"Device with UUID {uuid} not found."}
    if isinstance(sensor, Sensor) is False:
        return  {"error": f"Device with UUID {uuid} is not an sensor, meausrement can't be added."}
    #device is a sensor, and value can be added 
    value = measurement.newValue
    timestamp = measurement.newTimestamp
    unit = measurement.newSensorUnit
    
    #ts is optional, if not provided set it to time now
    if timestamp is None:
        timestamp = imestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #datetime.now() men som iso format ''2025-01-03 14:12:44''
        
    #create measurement OBS this function saves 
    repo.add_sensor_measurement_and_save(uuid,timestamp,value,unit)
    return {"message": "Measurmenet was successfully added"}
    #save the measurement in the repo    
    
    
@app.get("/smarthouse/sensor/{uuid}/values")
def get_n_last_measurements_or_all(uuid: str, limit : Optional[int] = None): #setter n til none dersom ikke definert.
    """GET smarthouse/sensor/{uuid}/values?limit=n - get n latest available measurements for sensor uuid.
    If query parameter not present, then all available measurements."""
    sensor = smarthouse.get_device_by_id(uuid) 
    if sensor is None:
        return {"error": f"Device with UUID {uuid} not found."}
    if isinstance(sensor, Sensor) is False:
        return  {"error": f"Device with UUID {uuid} is not an sensor, meausrement can't be read."}
    all_measurements = repo.get_all_sensor_readings(uuid)
    return all_measurements[:limit]


@app.delete("/smarthouse/device/{uuid}/oldest") #NOTICE i persistency, in the wuery, DESC wil delete newest, ASC will delete oldest.
def delete_oldest_measurement_by_device_id(uuid: str): 
    """
    This endpoints deletes oldest measurement from repo is sensor and has vale"""
    sensor = smarthouse.get_device_by_id(uuid) 
    if sensor is None:
        return {"error": f"Device with UUID {uuid} not found."}
    if isinstance(sensor, Sensor) is False:
        return  {"error": f"Device with UUID {uuid} is not an sensor, meausrement can't be deleted."}
    
    rowsAffectedd =repo.delete_oldest_measurements_and_save(sensor)
    if rowsAffectedd ==0:
        return {"message": "Nothing was deleted."}    
    
    return {"message": "Measurmenet was deleted"}
    #save the measurement in the repo       


@app.get("/smarthouse/actuator/{uuid}/current") 
def actuator_state_by_id(uuid: str):
    """
    This endpoint returns the current state for a device with type actuator with the given UUID.
    """
    # TODO ordne denne funksjonen med get device by ID!!!!!!!!!!!!!!!!!11
    device = smarthouse.get_device_by_id(uuid)  # Get all devices in the smarthouse    
    if isinstance(device, Actuator):  # Check if the device is an actuator
        state = repo.read_actuator_state(uuid)  # Get the actuator state
        if state is not None:  # Check if the state was found
            # return state #alternate... either 0 or 1
            return{
            'id': device.id,
            'state': state
            }
        return {"error": "No state found for this actuator."}
    return {"error": f"Device with UUID {uuid} not found in the smarthouse or not an actuator."}

# ####
# 'In a more structured design, consider using a Pydantic model 
#     to validate and encapsulate the input data for better error handling 
#     and automatic documentation.' Direct passing means filepath from bruno needs to be performed. 
#pydantic model means a basemodell have to be made.
# ####
#TODO usikker på om det er ment som smarthouse/device/{uuid} eller actutor.. 
@app.put("/smarthouse/device/{uuid}") 
def update_actuator_state(uuid: str, state_Update: ActuatorStateUpdate):
    actuator = smarthouse.get_device_by_id(uuid) 
    if actuator is None:
        return {"error": f"Device with UUID {uuid} not found."}
    if isinstance(actuator, Actuator) is False:
        return  {"error": f"Device with UUID {uuid} is not an actuator."}
    stateNew = state_Update.stateNewValid
    if stateNew >= 1: 
        actuator.turn_on()
    elif stateNew ==0:
        actuator.turn_off()
    else:
        return {"error": "Invalid state. Use 0 to turn off or 1 to turn on."}      
    repo.update_actuator_state(actuator) #update repo
    return {"message": "Actuator state updated successfully", "new_state": stateNew} #returns message to bruno  
        
    
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


