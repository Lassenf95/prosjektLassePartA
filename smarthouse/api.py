import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from smarthouse.persistence import SmartHouseRepository
from smarthouse.domain import SmartHouse, Room, Floor, Device, Sensor, Actuator, MIXActuatorSensor 
from pathlib import Path
from typing import Union
from pydantic import BaseModel
import os
def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

##### definering av basemodeller. Inspo fra løsningforslag
class ActuatorStateUpdate(BaseModel):
    stateNew: int



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
        floor_info.append(info) #etter en kjøring så legges til først level så ifnfom om hver rom i etasjen, gjentar dette for hver etajse
    #returner en dick der key/nøkkel er int(0..1..2 osv) og listens innhold(rom navn) er i string
    return {"floors": floor_info}


@app.get("/smarthouse/floor/{fid}")
def get_floor_info(fid: int): #-> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about the given floor in the smarthouse.
    """
    floors = smarthouse.get_floors()  # Henter ut alle etasjene
    # Gå gjennom etasjene for å finne den spesifikke etasje
    for floor in floors:
        if floor.level == fid:  # Sammenlign med ==
            floor_info ={
                "level": floor.level,
                "rooms": [room.room_name for room in floor.rooms]  # Liste over romnavn
            }
            return {'floor info': floor_info}
    # Hvis etasje ikke finnes, returner en feilmelding
    return {
        "error": f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen."
    }
    
@app.get("/smarthouse/floor/{fid}/room")
def get_rooms_on_floor(fid: int): #-> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns ann object that provides information
    about all the rooms in the given flor in the smarthouse.
    """
    room_info = []
    floors = smarthouse.get_floors()  # Get all the floor
    for floor in floors:
        if floor.level == fid:
            for rooms in floor.rooms:
                info= {
                    "room-name": rooms.room_name,
                    'room size': rooms.size,
                    'room id': rooms.id,
                    'room devices': [
                        {
                            'id': device.id,
                            'supplier': device.supplier,
                            'model_name': device.model_name,
                            'device type': device.device_type
                        } for device in rooms.devices
                    ]
                }
                room_info.append(info)
            return{'room info': room_info}        
        #Hvis etasje ikke finnes, returner en feilmelding
    return {
         "error": f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen."
     }

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
                    return {
                    "room-name": rooms.room_name,
                    'room size': rooms.size,
                    'room id': rooms.id,
                    'room devices': [
                        {
                            'id': device.id,
                            'supplier': device.supplier,
                            'model_name': device.model_name,
                            'device type': device.device_type
                        } for device in rooms.devices
                        ]
                    }
        return {
         "error": f"Rom id {rid} finnes ikke i level {fid}, prøv noe annet."
        }    
                       
    #Hvis etasje ikke finnes, returner en feilmelding
    return {
         "error": f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen."
     }
    

@app.get("/smarthouse/device")
def get_devices():# -> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about all the devices in the smarthouse
    """
    devices = smarthouse.get_devices()  # Get all devices in the smarthouse    
    result= []
    for device in devices:
        info = {   
                'room_name': device.room_name, #her er rommet til enheten
                'id': device.id,
                'supplier': device.supplier, 
                'model_name': device.model_name,
                'device_type': device.device_type
                }
        result.append(info)
    return result

    
@app.get("/smarthouse/device/{uuid}")
def get_device_by_id(uuid: str):# -> dict[str, Union[str, int, list[str]]]: 
    """
    This endpoint returns an object that provides information
    about the device with uuid = device.id
    """
    # TODO ordne denne funksjonen med get device by ID!!!!!!!!!!!!!!!!!11
    devices = smarthouse.get_devices()  # Get all devices in the smarthouse    
    for device in devices:
        if device.id == uuid:
            return {   
                'room_name': device.room_name, #her er rommet til enheten
                'id': device.id,
                'supplier': device.supplier, 
                'model_name': device.model_name,
                'device_type': device.device_type
                }
            
@app.get("/smarthouse/device/{uuid}/current")
def get_measurement_by_device_id(uuid: str): 
    """
    This endpoint returns the latest measurement for a device with the given UUID.
    """
    # TODO ordne denne funksjonen med get device by ID!!!!!!!!!!!!!!!!!11
    devices = smarthouse.get_devices()  # Get all devices in the smarthouse    
    for device in devices:
        if device.id == uuid:
            if isinstance(device, Sensor):
                measure = repo.get_latest_reading(device)
                return {
                        'timestamp': measure.timestamp,
                        'value': measure.value,
                        'unit': measure.unit
                    }
            return {"error": "No measurements found for this sensor."}
        return {"error": "The device is not a sensor and cannot provide measurements."}
    return {"error": f"Device with UUID {uuid} not found in the smarthouse."}

@app.get("/smarthouse/actuator/{uuid}/current") 
def get_current_actuator_state_by_id(uuid: str):
    """
    This endpoint returns the current state for a device with type actuator with the given UUID.
    """
    # TODO ordne denne funksjonen med get device by ID!!!!!!!!!!!!!!!!!11
    devices = smarthouse.get_devices()  # Get all devices in the smarthouse    
    for device in devices:
        if device.id == uuid:
            if isinstance(device, Actuator):  # Check if the device is an actuator
                state = repo.read_actuator_state(uuid)  # Get the actuator state
                if state is not None:  # Check if the state was found
                    return {
                        'id': device.id,
                        'state': state
                    }
                return {"error": "No state found for this actuator."}
    return {"error": f"Device with UUID {uuid} not found in the smarthouse or not an actuator."}

@app.put("/smarthouse/device/{uuid}") 
def update_actuator_state(uuid: str, state_Update: ActuatorStateUpdate):
    actuator = smarthouse.get_device_by_id(uuid) 
    if actuator is None:
        return {"error": f"Device with UUID {uuid} not found."}
    stateNew = state_Update.stateNew
    if stateNew >= 1: 
        actuator.turn_on()
    elif stateNew ==0:
        actuator.turn_off()  
    else:
        return {"error": "Invalid state. Use 0 to turn off or 1 to turn on."}      
    repo.update_actuator_state(actuator)
    return {"tilstand til aktuatoren er oppdater til": stateNew}    
        
    
    

#     for floor in floors:
# #         if floor.level == fid:  # Sammenlign med ==
# #             return {
# #                 "level": fid,
# #                 "levellll": floor.level,
# #                 "rooms": [room.room_name for room in floor.rooms]  # Liste over romnavn
# #             }
# #     # Hvis etasje ikke finnes, returner en feilmelding
# #     return {
# #         "error": f"Etasje med level {fid} finnes ikke i smarthuset, prøv en annen."
# #     }

    
    
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


