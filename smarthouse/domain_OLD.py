import random
from datetime import datetime
class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



class Floors:
    def __init__(self, level):
        self.level = level
        self.rooms = []#legger til en liste for alle rom


class Room:
    def __init__(self, level: Floors, size: float, name=None):
        self.level = level
        self.size = size
        self.name = name or f"Room at level {floor.level}"
        self.devices = [] #legger til en liste for alle enheter

    def add_device(self, device):
        self.devices.append(device)


class Devices:
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

        
class Sensor:
    def __init__(self, device: Devices, sensor_unit: str):
        self.device = device #assosiasjon, sensorene er en komponent
        self.sensor_unit = sensor_unit        
        self._last_measurement = None #første omgang helt udefinert, dvs none helt til noe annet er definert
        
    def get_last_measurement(self):
        """Dette må implementeres av subklassene."""
        raise NotImplementedError("Subklasser må implementere get_last_measurement()")

class TempSensor(Sensor):
    def __init__(self, device: Devices):
        #nå brukes arv. TempSensor isA(rv) Sensor. 
        super().__init__(device, "°C")  #skriver enhet direkte inn der ''sensor_unit'' står.
        
    def get_last_measurement(self):
        value = round(random.uniform(-10, 50), 1)  # tilfeldig verdi mellom -10 and 50grader
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class MotionSensor(Sensor):
    def __init__(self, device):
        super().__init__(device, "Bevegelse")  

    def get_last_measurement(self):
        value = random.choice([True, False])  # Tilfeldig True eller False
        timestamp = datetime.now().isoformat()
        measurement_value = "Bevegelse" if value else "Ingen bevegelse"
        return Measurement(timestamp, measurement_value, self.sensor_unit)
    
class HumidSensor(Sensor):
    def __init__(self, device):
        super().__init__(device, "%RH")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 100), 1)  # tilfeldig verdi mellom 0 til 100% RH luftfuktighet
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class CO2Sensor(Sensor):
    def __init__(self,device):
        super().__init__(device, "ppm")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 2000), 1)  # tilfeldig verdi mellom 0 til  2000 ppm co2 i lufta
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
class PowerSensor(Sensor):
    def __init__(self, device):
        super().__init__(device, "kw")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 3680), 1)  # tilfeldig verdi mellom 0 til 3680W i forbruk(utgangspunkt i bolig 16A*230V = 3680)
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class Actuator:
    def __init__(self, device, state: bool):
        self.device = device #assosiasjon, sensorene er en komponent
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
        self.floors = []
        self.rooms = []
        self.devices = []
        self.area = 0

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        level = Floors(level) 
        self.floors.append(level)
        return level

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(floor, room_size, room_name)
        self.rooms.append(room)
        pass

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        pass
 
    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        pass
    
    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        
    def get_devices(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.devices


    def register_device(self, room: Room, device: Devices):
        """
        This methods registers a given device in a given room.
        """
        device = Devices(room: Room, id: str, supplier_ str, model_name: str)
        self.devices.append(device)
        
        
    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass
        
    

    # def get_device_by_id(self, device_id: str) -> Devices | None:
    #     for device in self.devices:
    #         if device.id == device_id:
    #             return device
    #     return None

    # def get_floors(self) -> list:
    #     return sorted(self.floors, key=lambda x: x.level)

    # def get_rooms(self) -> list:
    #     return self.rooms

    # def get_area(self) -> float:
    #     return sum(room.size for room in self.rooms)

    # def register_device(self, room: Room, device: Devices):
    #     if room not in self.rooms:
    #         raise ValueError("Room is not registered in the house.")
    #     room.add_device(device)

    # def get_device(self, device_id: str) -> Devices | None:
    #     for room in self.rooms:
    #         for device in room.devices:
    #             if device.id == device_id:
    #                 return device
    #     return None

