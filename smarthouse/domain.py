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

class Devices():
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
        
        self.last_measurement = None #første omgang helt udefinert, dvs none helt til noe annet er definert
    def last_measurement(self):
        raise NotImplementedError("Subclasses must implement last_measurement") # todo fikse dette her 

class TempSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "°C")  #skriver enhet direkte inn der ''sensor_unit'' står. kunne evt definert denne  slik som i linje 32
        
    def last_measurement(self):
        value = round(random.uniform(-10, 50), 1)  # tilfeldig verdi mellom -10 and 50grader
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
class HumidSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "%RH")  
        
    def last_measurement(self):
        value = round(random.uniform(0, 100), 1)  # tilfeldig verdi mellom 0 til 100% RH luftfuktighet
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class CO2Sensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "%ppm")  
        
    def last_measurement(self):
        value = round(random.uniform(0, 2000), 1)  # tilfeldig verdi mellom 0 til  2000 ppm co2 i lufta
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
class PowerSensor(Sensor):
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name, "kw")  
        
    def last_measurement(self):
        value = round(random.uniform(0, 3680), 1)  # tilfeldig verdi mellom 0 til 3680W i forbruk(utgangspunkt i bolig 16A*230V = 3680)
        timestamp = datetime.now().isoformat()
        return Measurement(timestamp, value, self.sensor_unit)
    
class Actuator(Devices):
    def __init__(self, id: str, supplier: str, model_name: str), state:
        super().__init__(id, supplier, model_name)
        self.state = False
        self.target_value = None
    
    def turn_on(self):
        self.state = True
    
    def turn_off(self):
        self.state = False
    
    def is_active(self) -> bool:
        return self.state
    
class HeatPump(Actuator):
    """Heat pump actuator with adjustable set point."""
    def __init__(self, id: str, supplier: str, model_name: str, set_point: float = 20.0):
        super().__init__(id, supplier, model_name)
        self.set_point = set_point

    def set_temperature(self, value: float):
        self.set_point = value

class Furnace(Actuator):
    """Simple furnace actuator that can be turned on or off."""
    def __init__(self, id: str, supplier: str, model_name: str):
        super().__init__(id, supplier, model_name)
    
#Typer av sensorer(klasser som arver fra sensor):    
    

# class HumiditySensor(Sensor):
#     pass

# class TempSensor(Sensor):
#     pass

# class MotionSensor(Sensor):
#     pass

# class PowerSensor(Sensor):
#     pass

#Aktuatorer








class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
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


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        pass

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass

