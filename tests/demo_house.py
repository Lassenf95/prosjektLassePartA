from __future__ import annotations  # Gjør at rekkefølge av koden ikke har noe å si
import sys
import os
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from smarthouse.domain import SmartHouse, Sensor, Actuator, MIXActuatorSensor

# Create an instance of SmartHouse
FirstHouse = SmartHouse()

# Register the building
DEMO_HOUSE = SmartHouse.register_building('HVL')

# Building house structure
ground_floor = FirstHouse.register_floor(DEMO_HOUSE, 1)
second_floor = FirstHouse.register_floor(DEMO_HOUSE, 2)

# Register rooms in ground floor
entrance = FirstHouse.register_room(ground_floor, 13.5, "Entrance")
bathroom1 = FirstHouse.register_room(ground_floor, 6.3, "Bathroom1")
guestroom1 = FirstHouse.register_room(ground_floor, 8, "GuestRoom1")
livingroomKitchen = FirstHouse.register_room(ground_floor, 39.75, "livingroomKitchen")
garage = FirstHouse.register_room(ground_floor, 19, "garage")

# Register rooms in second floor
office = FirstHouse.register_room(second_floor, 11.75, "Office")
bathroom2 = FirstHouse.register_room(second_floor, 9.25, "Bathroom2")
guestroom2 = FirstHouse.register_room(second_floor, 8, "GuestRoom2")
hallway = FirstHouse.register_room(second_floor, 10, "Hallway")
guestroom3 = FirstHouse.register_room(second_floor, 10, "guestroom3")
dressingroom = FirstHouse.register_room(second_floor, 4, "dressingroom")
masterbedroom = FirstHouse.register_room(second_floor, 17, "masterBedroom")

# Create sensors and actuators
CO2_sensor = Sensor(id="8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", supplier="ElysianTech", model_name="Smoke Warden 1000", device_name='co2sensor', sensor_unit='ppm')
electricity_meter = Sensor(id="a2f8690f-2b3a-43cd-90b8-9deea98b42a7", supplier="MysticEnergy Innovations", model_name="Volt Watch Elite", device_name='energimaler', sensor_unit='kwh')
motion_sensor = Sensor(id="cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", supplier="NebulaGuard Innovations", model_name="MoveZ Detect 69", device_name='bevegelsensor', sensor_unit= 'movement')
humidity_sensor = Sensor(id="3d87e5c0-87f6-4b0b-9c67-087eaaed7b45", supplier="AetherCorp", model_name="Aqua Alert 800", device_name='fuktsesnor', sensor_unit='%RH')
temperature_sensor = Sensor("4d8b1d62-7921-4917-9b70-bbd316fe28e2", "AetherCorp", "SmartTemp 42", 'tempsensor', '°C')
air_quality_sensor = Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "CelestialSense Technologies", "AeroGuard Pro", 'luftkvalitetsensor', '%-kvalitet')

# Actuators
smart_lock = Actuator(id="4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", supplier="MythicalTech", model_name="Guardian Lock 7000", device_name='smart lock')
heat_pump = MIXActuatorSensor(id="5e13cabc-5c58-4bb3-82a2-3039e4480a6d", supplier="ElysianTech", model_name="Thermo Smart 6000", device_name='varmepumpe', sensor_unit='°C')
smart_oven = Actuator(id="8d4ea4c98-21a9-41e6-bf18-523285ad90f6", supplier="AetherCorp", model_name="Pheonix HEAT 333", device_name='smartOvn')
automatic_garage_door = Actuator(id="9a54c1ec-0cb5-45a7-b802-2a7394f1b132", supplier="MythicalTech", model_name="Guardian Lock 9000", device_name='garasjedor')
smart_plug = Actuator(id="1a66c3d6-22b2-446e-bf5c-eb59d18a87c9", supplier="MysticEnergy Innovations", model_name="FlowState X", device_name='smart plug')
dehumidifier = Actuator(id="9e5b8274-4e77-4e4e-80d2-b04d648ea02a", supplier="ArcaneTech Solutions", model_name="Hydra Dry 8000", device_name='avfukter')
light_bulb = Actuator(id="6b1c5f6b-37f6-4e3d-9145-1cfbe2f1f2c8", supplier="Elysian Tech", model_name="Lumina Glow 4000", device_name='Light bulp')

# Register devices in rooms
FirstHouse.register_device(garage, automatic_garage_door)
FirstHouse.register_device(guestroom1, smart_oven)
FirstHouse.register_device(bathroom1, humidity_sensor)
FirstHouse.register_device(entrance, smart_lock)
FirstHouse.register_device(entrance, electricity_meter)
FirstHouse.register_device(livingroomKitchen, heat_pump)
FirstHouse.register_device(livingroomKitchen, motion_sensor)
FirstHouse.register_device(livingroomKitchen, CO2_sensor)

# Register devices in second floor rooms
FirstHouse.register_device(guestroom2, light_bulb)
FirstHouse.register_device(bathroom2, dehumidifier)
FirstHouse.register_device(office, smart_plug)
FirstHouse.register_device(guestroom3, air_quality_sensor)
FirstHouse.register_device(masterbedroom, temperature_sensor)
FirstHouse.register_device(masterbedroom, smart_oven)