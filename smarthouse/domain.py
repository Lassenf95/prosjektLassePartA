from __future__ import annotations #slik at rekkefølge av koden ikke har noe å si
import random
from datetime import datetime
from typing import List, Optional, Union 

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class Building:
    def __init__(self, address: str):
        self.address= address
        self.floors: List[Floor] = [] # Assosiasjon. Bynigng has-a floor       
class Floor: #hver bygning inneholder etasjer
    def __init__(self, level: int):
        self.level = level
        self.rooms: List[Room] = [] #Assosiasjon. Etasje has a room.
class Room: #hver etasje inneholder rom/flere room definert under Floor
    def __init__(self, floor: Floor, size: float, name=None):
        self.floor: Floor = floor
        self.size: float = size
        self.name: str = name
        self.devices: List[Device] = [] #assosiasjon. Room has a device.     
           
class Device: #hvert rom inneholder devicer deifnert under Room. Device er superklasse for både sensorer og aktuatorer
    def __init__(self, id: str, supplier: str, model_name: str, device_name: str):
        self.id= id
        self.supplier= supplier
        self.model_name= model_name
        self.device_name = device_name #lånt fra LF istedenfor å ha en ny klasse for hver eneste type av sensorer.. 
     #Lånt det under fra fasit TODO FJERNE      
    def is_sensor(self) -> bool:
        return True 
    
    def is_actuator(self) -> bool:
        return False
    
    def last_measurement(self) -> Measurement:
        return Measurement(datetime.now().isoformat(), random() * 10, self.unit)

class Sensor(Device): #sensorer is-a device. Arver
    def __init__(self, id: str, supplier: str, model_name: str, device_name:str,  sensor_unit: str):
        super().__init__(id, supplier, model_name,device_name) 
        self.sensor_unit = sensor_unit  #her defineres målenehten til sensoren.

    
    def get_last_measurement(self):
        value = round(random.uniform(0, 100), 1)  # tilfeldig verdi mellom 0 til 100
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    

class Actuator(Device): #Actuator er en device. Arver(is a)
    def __init__(self, id: str, supplier: str, model_name: str, device_name: str):
        super().__init__(id,supplier,model_name, device_name)
        self.state = False #default til av før noe annet er nevnt
    
    #Lånt det under fra fasit TODO FJERNE     
    def is_actuator(self) -> bool:
        return True

    def is_sensor(self) -> bool:
        return False

    def turn_on(self, target_value: Optional[float] = None):
        if target_value:
            self.state = target_value
        else:
            self.state = True

    def turn_off(self):
        self.state = False 

    def is_active(self) -> bool:
        return self.state is not False

# c#lass CombiActuatorSensor(Actuator, Sensor):
#     def __init__(self, id: str, supplier: str, model_name: str, device_name: str, sensor_unit: str):
#         Actuator.__init__(self, id, supplier, model_name, device_name)
#         Sensor.__init__(self, id, supplier, model_name, device_name, sensor_unit)
#         #self.sensor_unit = sensor_unit
#         self.state = False  # default til av før noe annet er nevnt
#     # TODO lånt fra løsningsforslag 
#   
# 
# 
class MIXActuatorSensor(Device):
    def __init__(self, id: str, supplier: str, model_name: str, device_name: str, sensor_unit: str):
        super().__init__(id, supplier, model_name, device_name)
        self.sensor_unit = sensor_unit
        self.state = False
    def is_actuator(self) -> bool:
        return True

    def is_sensor(self) -> bool:
        return True


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """    
    #egenskaper/attributer ved enhvert smarthus
    def __init__(self):
        self.buildings: List[Building] = [] #ethvert instans av smarthus er en bygning

    def register_building(self, address: str):
        new_buidling = Building(address)
        self.buildings.append(new_buidling)
        return new_buidling       
        
    def register_floor(self, building: Building, level:int):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        #tanken er her at et nytt floor lages, når en ny etasje lages, så skal også det lages en ny tilhørende liste av rom til denne etasjen
        new_floor = Floor(level) #skaper en ny etasje
        building.floors.append(new_floor) #legger til en ny etasje i bygningen
        return new_floor

    def register_room(self, floor: Floor, room_size, room_name):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        new_room = Room(floor, room_size, room_name)
        floor.rooms.append(new_room) #legger til det nye rommet i etasjen sin egen liste over rom
        return new_room
        #et nytt rom er dannet, og det må plasseres i listen av rom, for den gitte etasje
        #self.rooms.append(newRoom)
        


    def get_floors(self, building: Building):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return sorted(building.floors, key=lambda f: f.level)



    def get_rooms(self, building: Building):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        rooms = []
        for floor in building.floors:
            rooms.extend(floor.rooms)  # Samler alle rom fra hver etasje
        return rooms


    def get_area(self, building: Building):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(room.size for floor in building.floors for room in floor.rooms)


    def register_device(self, room: Room, device: Device):
        """
        This methods registers a given device in a given room. 
        """
        #USIKKER PÅ OM DET HER ER MENT AT ENHTEN ALLEREDE EKSITERER, MEN IKKE ER PLASSSER
        #koden under registrerer en eksistrende enhet i et eksiterende rom
        room.devices.append(device) #legger enhete i det eksistrerende rommet
       
    def get_devices(self, building: Building):
        """
        This method retrieves a list of all devices 
        """
        devices= []
        for floor in building.floors: #for det aktuelle bygget er det flere etasjer
            for room in floor.rooms: #for hver etasje er det flere rom
                devices.extend(room.devices)                   
        return devices
        
    def get_devices_by_id(self, building: Building, device_id):
      
        for floor in building.floors: #for det aktuelle bygget er det flere etasjer
            for room in floor.rooms: #for hver etasje er det flere rom
                for device in room.devices: # for hvert rom kan det være flere ID
                    if device.id == device_id: 
                        return device
        return None #ingenting dersom ingen devicer mathcher