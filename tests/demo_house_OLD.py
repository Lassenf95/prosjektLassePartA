from __future__ import annotations  # Gjør at rekkefølge av koden ikke har noe å si
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smarthouse.domain import SmartHouse, Actuator, Sensor, Device, HumiditySensor, CO2Sensor,PowerSensor,MotionSensor,TempSensor
from typing import List

DEMO_HOUSE = SmartHouse()

#Bygger så smart huset mitt. Dette er veldig manuelt utført i første omgang. Se bilde for prosjektet med 2 etasjer. Senere kan det tenkes at det det lages et GUI ens for dette slik det er lettere å lage flere hus/bygg.

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)


#rommene i første etasje registreres
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
bathroom1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom1")
guestroom1 = DEMO_HOUSE.register_room(ground_floor, 8, "GuestRoom1")
livingroomKitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "livingroomKitchen")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "garage")

#rommene i andre etasje registreres
office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bathroom2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom2")
guestroom2 = DEMO_HOUSE.register_room(second_floor, 8, "GuestRoom2")
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
guestroom3 = DEMO_HOUSE.register_room(second_floor, 10, "guestroom3")
dressingroom = DEMO_HOUSE.register_room(second_floor, 4, "dressingroom")
masterbedroom = DEMO_HOUSE.register_room(second_floor, 17, "masterBedroom")

#først enkle sensorer

# Sensorer
CO2_sensor = CO2Sensor(id="8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", supplier="ElysianTech", model_name="Smoke Warden 1000")
electricity_meter = PowerSensor(id="a2f8690f-2b3a-43cd-90b8-9deea98b42a7", supplier="MysticEnergy Innovations", model_name="Volt Watch Elite")
motion_sensor = MotionSensor(id="cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", supplier="NebulaGuard Innovations", model_name="MoveZ Detect 69")
humidity_sensor = HumiditySensor(id="3d87e5c0-87f6-4b0b-9c67-087eaaed7b45", supplier="AetherCorp", model_name="Aqua Alert 800")
temperature_sensor = TempSensor(id="4d8b1d62-7921-4917-9b70-bbd316fe28e2", supplier="AetherCorp", model_name="SmartTemp 42")
# air_quality_sensor = Sensor(id="7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", supplier="CelestialSense Technologies", model_name="AeroGuard Pro")

# Aktuatorer
#smart_lock = Actuator(id="4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", supplier="MythicalTech", model_name="Guardian Lock 7000")
#heat_pump = Actuator(id="5e13cabc-5c58-4bb3-82a2-3039e4480a6d", supplier="ElysianTech", model_name="Thermo Smart 6000")
#smart_oven = Actuator(id="8d4ea4c98-21a9-41e6-bf18-523285ad90f6", supplier="AetherCorp", model_name="Pheonix HEAT 333")
#automatic_garage_door = Actuator(id="9a54c1ec-0cb5-45a7-b802-2a7394f1b132", supplier="MythicalTech", model_name="Guardian Lock 9000")
#smart_plug = Actuator(id="1a66c3d6-22b2-446e-bf5c-eb59d18a87c9", supplier="MysticEnergy Innovations", model_name="FlowState X")
#dehumidifier = Actuator(id="9e5b8274-4e77-4e4e-80d2-b04d648ea02a", supplier="ArcaneTech Solutions", model_name="Hydra Dry 8000")
# light_bulb = Actuator(id="6b1c5f6b-37f6-4e3d-9145-1cfbe2f1f2c8", supplier="Elysian Tech", model_name="Lumina Glow 4000")

# Registrerer enhten av typen i første etasje
# DEMO_HOUSE.register_device(garage, automatic_garage_door)
# DEMO_HOUSE.register_device(guestroom1, smart_oven)
DEMO_HOUSE.register_device(bathroom1, humidity_sensor)
# DEMO_HOUSE.register_device(entrance, smart_lock)
DEMO_HOUSE.register_device(entrance, electricity_meter)
# DEMO_HOUSE.register_device(livingroomKitchen, heat_pump)
DEMO_HOUSE.register_device(livingroomKitchen, motion_sensor)
DEMO_HOUSE.register_device(livingroomKitchen, CO2_sensor)

#andre etasje
#DEMO_HOUSE.register_device(guestroom2, light_bulb)
#DEMO_HOUSE.register_device(bathroom2, dehumidifier)
#DEMO_HOUSE.register_device(office,smart_plug)
#DEMO_HOUSE.register_device(guestroom3, air_quality_sensor)
DEMO_HOUSE.register_device(masterbedroom, temperature_sensor)
#DEMO_HOUSE.register_device(masterbedroom, smart_oven)

#så enkle aktuatorer
# så kombinasjonene:

print(DEMO_HOUSE.devices)  
print(bathroom1.devices)
