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
    def __init__(self, id: str, supplier: str, model_name: str, device_type: str):
        self.room_name = None   #ved opprettelse av devier så må rom attributtene tildeles senere når devicen blir plassert
        self.id= id
        self.supplier= supplier
        self.model_name= model_name
        self.device_type = device_type #lånt fra LF istedenfor å ha en ny klasse for hver eneste type av sensorer..
        #self.room = None  # Add this line to initialize the room attribute 
     #Lånt det under fra fasit TODO FJERNE      
     
    def to_dict(self) -> str:
        return{ 'room_name': self.room_name, #her er rommet til enheten
                'id': self.id,
                'supplier': self.supplier, 
                'model_name': self.model_name,
                'device_type': self.device_type,
                
            }
            
            
        
    
    def get_device_type(self) -> str:
        return self.device_type
    
    
    def is_actuator(self) -> bool:
        pass

    def is_sensor(self) -> bool:
        pass
    
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
    def __init__(self, id: str, supplier: str, model_name: str, device_type:str,  sensor_unit: str):
        super().__init__(id, supplier, model_name,device_type) 
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
    def __init__(self, id: str, supplier: str, model_name: str, device_type: str):
        super().__init__(id,supplier,model_name, device_type)
        self.state: Union[bool, float, int] = False #default til av før noe annet er nevnt
        self.sensor_unit= None #
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
#     def __init__(self, id: str, supplier: str, model_name: str, device_type: str, sensor_unit: str):
#         Actuator.__init__(self, id, supplier, model_name, device_type)
#         Sensor.__init__(self, id, supplier, model_name, device_type, sensor_unit)
#         #self.sensor_unit = sensor_unit
#         self.state = False  # default til av før noe annet er nevnt
#     # TODO lånt fra løsningsforslag 
#   
# 

class MIXActuatorSensor(Device) : #Actuator, Sensor): TODO fikse denne med arv...
    def __init__(self, id: str, supplier: str, model_name: str, device_type: str, sensor_unit: str):
        #Actuator.__init__(self, id, supplier, model_name, device_type)
        #Sensor.__init__(self, id, supplier, model_name, device_type, sensor_unit)
        super().__init__(id, supplier, model_name, device_type)
        self.sensor_unit = sensor_unit
        self.state = False  # default til av før noe annet er nevnt

    def is_actuator(self) -> bool:
        return True

    def is_sensor(self) -> bool:
        return True
    
    def turn_on(self, target_value: Optional[float] = None):
       if target_value:
           self.state = target_value
       else:
           self.state = True
           
    def turn_off(self):
        self.state = False 
    
    def is_active(self) -> bool:
        return self.state is not False


# class Building:
#     def __init__(self, address: str):
#         self.address= address
#         self.floors: List[Floor] = [] # Assosiasjon. Bynigng has-a floor       
class Floor: #hver bygning inneholder etasjer
    def __init__(self, level: int):
        self.level = level
        self.rooms: List[Room] = [] #Assosiasjon. Etasje has a room.
          
    
class Room: #hver etasje inneholder rom/flere room definert under Floor
    def __init__(self, floor: Floor, size: float, room_name: str):
        self.floor: Floor = floor
        self.size: float = size
        self.room_name: str = room_name
        self.devices: List[Device] = [] #assosiasjon. Room has a device.     
        
        #OBS DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB
        self.id = None  # ID er ikke kjent ved opprettelse

    def set_id(self, room_id):
            self.id = room_id
#OBS DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB DELB


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
        roomListe: list[Room] = []
        for floor in self.floors: #for hver etasje i huset
            for eachRoom in floor.rooms:   #for hvert rom i etasjen
             roomListe.append(eachRoom)    #legger til rommene i listen over rom
        return roomListe #returnerer listen over rom helt til slutt

        # devices = []
        # for floor in self.floors:
        #     for room in floor.rooms:
        #         devices.extend(room.devices)
        # return devices

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
        
        #SJEKKER FØRST OM ENHETEN ALLEREDE Finnes i et annet rom
        #vet at dersom en enhet er laget, men ikke tildelt, så er navnet none
        #vet at dersom en enhet er laget, men ikke tildelt,
        if device.room_name is not None: #enheten er tildelt er rom, nå må enheten slettes, og fjernes fra rommet.
            for eachFloor in self.floors: #for hver etasje i huset
                for eachRoom in eachFloor.rooms: #for hvert rom i etasjen
                    if device in eachRoom.devices: #dersom enheten er i rommet
                        eachRoom.devices.remove(device)
                        
            # if device in device.room.devices: #dersom enheten er i rommet
            #     device.room.devices.remove(device) #fjerner enheten fra rommet
                
        # Add the device to the room
        room.devices.append(device) #legger til en device i rommet
        #device.roomName = room.name #tilordner rommet attributtene til rom enheten7
        device.room = room 
        device.room_name = room.room_name
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
       #husk at SELF er demohus, slik at self.floors.rooms.devices der devices er nivå vil vi hente ut
        deviceListe: list[Device] = []
        for eachFloor in self.floors:   #for hver etasje
            for eachRoom in eachFloor.rooms:   #for hvert rom
                for eachDevice in eachRoom.devices: #for hvert rom
                    deviceListe.append(eachDevice)   #legges enheten i listen over enheter
        return deviceListe #returnere til slutt listen

 
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
            
    