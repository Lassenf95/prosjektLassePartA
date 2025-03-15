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

class Devices:
    def __init__(self, id: str, supplier: str, model_name: str):
        self.id= id
        self.supplier= supplier
        self.model_name= model_name
        
    def is_actuator(self):
        return isinstance(self, Actuator)
    
    def is_sensor(self):
        return isinstance(self, Sensor)
        
    def get_device_type(self):
        return self.__class__.__name__
        
#sensorer og aktuatorer er sub-klasser av ''devices''' og arver egenskapene fra devices. I tilegg bruker super(). for å egge til attributes
class Sensor(Devices): #base klasse for alle sensorer
    def __init__(self, id: str, supplier: str, model_name: str, sensor_unit: str):
        super().__init__(id,supplier,model_name)
        self.sensor_unit = sensor_unit
        
        self._last_measurement = None #første omgang helt udefinert, dvs none helt til noe annet er definert
    def last_measurement(self):
        raise NotImplementedError("Subclasses must implement last_measurement") # todo fikse dette her 

class TempSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "°C")  #skriver enhet direkte inn der ''sensor_unit'' står. kunne evt definert denne  slik som i linje 32
        
    def get_last_measurement(self):
        value = round(random.uniform(-10, 50), 1)  # tilfeldig verdi mellom -10 and 50grader
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class motion_sensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "Bevegelse")  

    def get_last_measurement(self):
        value = random.choice([True, False])  # Tilfeldig True eller False
        timestamp = datetime.now().isoformat()
        measurement_value = "Bevegelse" if value else "Ingen bevegelse"
        return Measurement(timestamp, measurement_value, self.sensor_unit)
    
class HumidSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "%RH")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 100), 1)  # tilfeldig verdi mellom 0 til 100% RH luftfuktighet
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class CO2Sensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "ppm")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 2000), 1)  # tilfeldig verdi mellom 0 til  2000 ppm co2 i lufta
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
class PowerSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "kw")  
        
    def get_last_measurement(self):
        value = round(random.uniform(0, 3680), 1)  # tilfeldig verdi mellom 0 til 3680W i forbruk(utgangspunkt i bolig 16A*230V = 3680)
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class Actuator(Devices):
    def __init__(self, id: str, supplier: str, model_name: str, state: bool):
        super().__init__(id, supplier, model_name)
        self.state = False #default til av før noe annet er nevnt
    
    def turn_on(self):
        self.state = True
    
    def turn_off(self):
        self.state = False
    
    def is_active(self) -> bool:
        return self.state
    
class HeatPump(Actuator):
    def __init__(self, id: str, supplier: str, model_name: str, state:bool, set_point: float = 20.0): #varmepumpe med variabelt set punkt
        super().__init__(id, supplier, model_name, state)
        self.set_point = set_point

    def target_value(self, value: float): #dersom bruker ønkser å endre set punktet skrives nytt setpunkt inn
        self.set_point = value


class Bulp(Actuator):
    #av eller på eller slå på
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name)

class Furnace(Actuator):
    """Simple furnace actuator that can be turned on or off."""
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name)
    





class Floor():
    def __init__(self, level):
        self.level = level
        self.rooms = []

class Room():
    def __init__(self, floor, size, name=None):
        self.floor = floor
        self.size = size
        self.name = name or f"Room at level {floor.level}"
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)



class SmartHouse:
    def __init__(self):
        self.floors = []  # Holder styr på registrerte etasjer
        self.devices = []  # Holder styr på registrerte etasjer
        self.rooms = []   # Holder styr på registrerte rom
        self.area = 0  # Størrelse på huset
         
    def register_floor(self, level):
        if level in [floor.level for floor in self.floors]:  # Sjekk om etasjen allerede finnes
            raise ValueError(f"Floor with level {level} already exists.")
        floor = Floor(level)  # Oppretter etasje
        self.floors.append(floor)  # Legger til i listen over etasjer
        return floor

    def register_room(self, floor, room_size, room_name=None):
        if floor not in self.floors:
            raise ValueError("Floor is not registered in the house.")
        room = Room(floor, room_size, room_name)  # Oppretter rom
        self.rooms.append(room)  # Legger til i listen over rom
        return room

    def get_devices(self):
        return self.devices

    def get_device_by_id(self, device_id):
        for device in self.devices:
            if device.id == device_id:
                return device
        return None
    def get_floors(self):
        return sorted(self.floors, key=lambda x: x.level)  # Returnerer etasjer sortert etter nivå

    def get_rooms(self):
        return self.rooms  # Returnerer alle rom

    def get_area(self):
        return sum(room.size for room in self.rooms)  # Summerer arealene til alle rommene

    def register_device(self, room, device):
        if room not in self.rooms:
            raise ValueError("Room is not registered in the house.")
        room.add_device(device)

    def get_device(self, device_id):
        for room in self.rooms:
            for device in room.devices:
                if device.id == device_id:
                    return device
        return None  # Returnerer None hvis enheten ikke finnes
