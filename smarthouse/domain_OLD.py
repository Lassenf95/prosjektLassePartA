import random
from datetime import datetime
from __future__ import annotations #slik at rekkefølge av koden ikke har noe å si
from typing import List 



class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit    
    
# class Building:
#     def __init__(self, address: string):
#         self.address = address
#         return Building


class Building:
    def __init__(self, adress: str):
        self.adress= adress
        self.floors: List[Floor] = [] # hver bygning har har etasje(r)
    
class Floor: #hver bygning inneholder etasjer
    def __init__(self, level: int):
        self.level = level
        self.rooms: List[Room] = [] #hver etasje inneholder en ny liste av rom


class Room: #hver etasje inneholder rom/flere room
    def __init__(self, level: Floor, size: float, name=None):
        self.level: Floor = level
        self.size: float = size
        self.name: str = name
        self.devices = [] #hvert rom har sin egen liste over enheter i rommet 
        
    def add_device(self, device: Device): 
        self.devices.append(device)


class Device: #hvert rom inneholder devicer
    def __init__(self, room : Room, id: str, supplier: str, model_name: str):
        self.room = room # assosiasjon til et rom, ikke arving
        self.id= id
        self.supplier= supplier
        self.model_name= model_name
        
        
    def is_actuator(self):
        return isinstance(self, Actuator)
    
    def is_sensor(self):
        return isinstance(self, Sensor)
        
    def get_device_type(self):
        return self.__class__.__name__

        
class Sensor(Device): #sensoer er en device. Arver(is a)
    def __init__(self, room: Room, id: str, supplier: str, model_name: str, sensor_unit: str):
        super().__init__(room, id, supplier, model_name)
        self.sensor_unit = sensor_unit        
        self._last_measurement = None #første omgang helt udefinert, dvs none helt til noe annet er definert
        
    def get_last_measurement(self):
        """Dette må implementeres av subklassene."""
        raise NotImplementedError("Subklasser må implementere get_last_measurement()")


class HumiditySensor(Sensor):
    def __init__(self, room, id, supplier,model_name):
        super().__init__(room,id,supplier, model_name, "%RH")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 100), 1)  # tilfeldig verdi mellom 0 til 100% RH luftfuktighet
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    

class TempSensor(Sensor):
    def __init__(self, room, id, supplier,model_name):
        #nå brukes arv. TempSensor isA(rv) Sensor. 
        super().__init__(room,id,supplier, model_name,"°C")  #skriver enhet direkte inn der ''sensor_unit'' står.
        
    def get_last_measurement(self):
        value = round(random.uniform(-10, 50), 1)  # tilfeldig verdi mellom -10 and 50grader
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class MotionSensor(Sensor):
    def __init__(self, room, id, supplier,model_name):
        super().__init__(room,id,supplier, model_name, "Bevegelse")  

    def get_last_measurement(self):
        value = random.choice([True, False])  # Tilfeldig True eller False
        timestamp = datetime.now().isoformat()
        measurement_value = "Bevegelse" if value else "Ingen bevegelse"
        return Measurement(timestamp, measurement_value, self.sensor_unit)
    

    
class CO2Sensor(Sensor):
    def __init__(self, room, id, supplier,model_name):
        super().__init__(room,id,supplier, model_name, "ppm")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 2000), 1)  # tilfeldig verdi mellom 0 til  2000 ppm co2 i lufta
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
class PowerSensor(Sensor):
    def __init__(self, room, id, supplier,model_name):
        super().__init__(room,id,supplier, model_name, "kw")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 3680), 1)  # tilfeldig verdi mellom 0 til 3680W i forbruk(utgangspunkt i bolig 16A*230V = 3680)
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class Actuator(Device): #Actuator er en device. Arver(is a)
    def __init__(self, room: Room, id: str, supplier: str, model_name: str, state: bool = False):
        super().__init__(room,id,supplier,model_name)
        self.state = False #default til av før noe annet er nevnt
    
    def turn_on(self):
        self.state = True
    
    def turn_off(self):
        self.state = False
    
    def is_active(self) -> bool:
        return self.state
    
# class HeatPump(Actuator):
#     def __init__(self, device, state, set_point: float = 20.0): #varmepumpe med variabelt set punkt
#         super().__init__(id, supplier, model_name, state)
#         self.set_point = set_point

#     def set_target_value(self, value: float): #dersom bruker ønkser å endre set punktet skrives nytt setpunkt inn
#         self.set_point = value


# class Bulp(Actuator):
#     def __init__(self, id, supplier, model_name, state: bool = False):
#         super().__init__(id, supplier, model_name, state)

# class Furnace(Actuator):
#  def __init__(self, id, supplier, model_name, state: bool = False):
#         super().__init__(id, supplier, model_name, state)
    


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self):
        self.floors: List[Floor] = []  # Eksplisitt liste av Floor-objekter. kunne abstrahert og skrevet self.floors = []
        self.rooms: List[Room] = []    # Eksplisitt liste av Room-objekter
        self.devices: List[Device] = []  # Eksplisitt liste av Device-objekter
        self.area = 0

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        level = Floor(level) #danner en ny etasje
        self.floors.append(level) # registrer enda en etasje med det gitte nivået
        return level #returnerer etasjenummeret

    def register_room(self, floor, room_size, room_name):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(floor, room_size, room_name) #danner rommet utifra etasje, arealet og navnet
        floor.rooms.append(room) #legger til rommet i etasjen det tilhører
        room.rooms.append(room) #legger til rommet i listen over rom
        return room #returner romet

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.floors
 
    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        return self.rooms
        
    
    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        totaltAreal = 0
        for each_room in self.rooms:
            totaltAreal += each_room.areal 
        return totaltAreal
        
        
 
    def register_device(self, room: Room, id: str, supplier: str, model_name: str):
        """
        This methods registers a given device in a given room. Input argumentene er et rom og en enhet,
        """      
        newDevice = Device(room, id, supplier,model_name)  
        room.add_device(newDevice) #legger til en device i rommet
        self.devices.append(newDevice) #i listen over enheter legges til en ny enhet
        return newDevice
        

      
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass
        
