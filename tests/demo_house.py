import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from smarthouse.domain import SmartHouse
from smarthouse.domain import Actuator
from smarthouse.domain import Sensor

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)


#rommene i første etasje registreres
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
bathroom1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom1")
guestroom1 = DEMO_HOUSE.register_room(ground_floor, 8, "GuestRoom1")
livingroomKitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "livingroomKitchen")

#rommene i andre etasje registreres
office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bathroom2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom2")
guestroom2 = DEMO_HOUSE.register_room(second_floor, 8, "GuestRoom2")
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
questroom3 = DEMO_HOUSE.register_room(second_floor, 10, "guestroom3")
dressingroom = DEMO_HOUSE.register_room(second_floor, 4, "dressingroom")
masterbedroom = DEMO_HOUSE.register_room(second_floor, 17, "masterBedroom")

#enhetene i første etasje registreres
SmartLock = Actuator(id="4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", supplier="MythicalTech", model_name= "Guardian Lock 7000")
SmartHouse.register_device(entrance,SmartLock)

#først enkle sensorer

#så enkle aktuatorer

# så kombinasjonene:

#CO2Sensor = Sensor(id='',supplier='',model_name='')





#enhetene i første etasje registreres

DEMO_HOUSE.register_device(entrance,  )



# TODO: continue registering the remaining floor, rooms and devices

