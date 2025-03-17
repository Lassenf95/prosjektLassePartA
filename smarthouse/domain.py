from __future__ import annotations #slik at rekkefølge av koden ikke har noe å si
import random
from datetime import datetime
from typing import List, Optional, Union 
from abc import abstractmethod

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



# TODO: Add your own classes here!

class Device: #hvert rom inneholder devicer deifnert under Room. Device er superklasse for både sensorer og aktuatorer
    def __init__(self, id: str, supplier: str, model_name: str, device_name: str):
        self.room = None   #ved opprettelse av devier så må rom attributtene tildeles senere når devicen blir plassert
        self.id= id
        self.supplier= supplier
        self.model_name= model_name
        self.device_name = device_name #lånt fra LF istedenfor å ha en ny klasse for hver eneste type av sensorer..
        #self.room = None  # Add this line to initialize the room attribute 
     #Lånt det under fra fasit TODO FJERNE      
   
    def get_device_type(self) -> str:
        return self.device_name
    
    
    def is_actuator(self) -> bool:
        return False

    def is_sensor(self) -> bool:
        return False
    
    #     return True 
    
    # def is_actuator(self) -> bool:
    #     return False
    
    # def last_measurement(self) -> Measurement:
    #     return Measurement(datetime.now().isoformat(), random() * 10, self.unit)
    # @abstractmethod
    # def is_actuator(self) -> bool:
    #     pass

    # @abstractmethod
    # def is_sensor(self) -> bool:
    #     pass

class Sensor(Device): #sensorer is-a device. Arver
    def __init__(self, id: str, supplier: str, model_name: str, device_name:str,  sensor_unit: str):
        super().__init__(id, supplier, model_name,device_name) 
        self.sensor_unit = sensor_unit  #her defineres målenehten til sensoren.

    def is_sensor(self):
        return True
    
    def is_actuator(self):
        return False
    
    def last_measurement(self):
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
class MIXActuatorSensor(Actuator, Sensor):
    def __init__(self, id: str, supplier: str, model_name: str, device_name: str,sensor_unit: str): 
        super().__init__(id, supplier, model_name,device_name)
        self.sensor_unit = sensor_unit
        self.state = False  # default til av før noe annet er nevnt
        
    #def __init__(self, id: str, supplier: str, model_name: str, device_name: str, sensor_unit: str):
     #   Actuator.__init__(self, id, supplier, model_name, device_name)
      #  Sensor.__init__(self, id, supplier, model_name, device_name,sensor_unit=sensor_unit)
       # self.state = False  # Sikrer at aktuator-delen starter i AV-tilstand
        #self.sensor_unit = sensor_unit
       
    def is_actuator(self) -> bool:
        return True

    def is_sensor(self) -> bool:
        return True
    
    def turn_on(self, target_value: Optional[float] = None):
       if target_value:
           self.state = target_value
       else:
           self.state = True




# class Building:
#     def __init__(self, address: str):
#         self.address= address
#         self.floors: List[Floor] = [] # Assosiasjon. Bynigng has-a floor       
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

class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

#  #egenskaper/attributer ved enhvert smarthus
#     def __init__(self):
#         self.buildings: List[Building] = [] #ethvert instans av smarthus er en bygning

#     def register_building(self, address: str):
#         new_buidling = Building(address)
#         self.buildings.append(new_buidling)
#         return new_buidling
    
    def __init__(self):
        self.floors: list[Floor] = [] #for hver instans av et hus/bygning så har vi etasje(r)

    

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        new_floor = Floor(level) #skaper en etasje
        self.floors.append(new_floor) #registrerer en ny etasje med det gitte nivået
        return new_floor

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        new_room = Room(floor, room_size, room_name) #skaper et nytt rom
        floor.rooms.append(new_room) #registrerer et nytt rom i etasjen sin egen liste over rom
        return new_room


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return sorted(self.floors, key=lambda f: f.level)


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        rooms = []
        for floor in self.floors:
            rooms.extend(floor.rooms)
        return rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(room.size for floor in self.floors for room in floor.rooms)


    def register_device(self, room: Room, device: Device):
        """
        This methods registers a given device in a given room.
        """ 
        #under demo_house.py er allerede enhetene laget, så her skal vi bare legge til enhetene i rommenes liste over enheter
        room.devices.append(device) #legger til en device i rommet
        #device.roomName = room.name #tilordner rommet attributtene til rom enheten7
        device.room = room
        return device 
    
    def get_devices(self):
        """
        This method retrieves a list for all devices in the house.
        """
        # listeAvEnhter:  list[Device] = []
        # for floor in self.floors: #for hver etasje i huset
        #     for room in floor.rooms: #for hvert rom i etasjen
        #         for device in room.devices: #for hver enhet i rommet
        #             listeAvEnhter.append(device) #legger til enheten i listen over enheter       
        # return listeAvEnhter #returner så til slutt listen av alle enehtene
    
        devices = []
        for floor in self.floors:
            for room in floor.rooms:
                devices.extend(room.devices)
        return devices

 
    def get_device_by_id(self, device_id: str):
        """
        This method retrieves a device object via its id.
        """
        targetID = device_id #dette er iden jeg søker etter
        for floor in self.floors:   #for alle etasjer skal jeg søke i...
            for room in floor.rooms: #alle rommene i den gitte etasajse
                for device in room.devices: #etter alle enhetene i det gitte rommet
                    if device.id == targetID: #her til det matcher
                        return device #returner enheten dersom det eksiterer en match
        return None #dersom ingen match oppstår kjører koden her og returner ingenting...         
            
    