import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common

print("Starter smarthouse_temperature_sensor.py")
logging.basicConfig(level=logging.INFO)


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')
        self.lock = threading.Lock()  # lock to avvoid race contions
        # if reading and writing sensor dato may occur at the same time 

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:
            with self.lock:
                temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)
                logging.info(f"Sensor {self.did}: {temp}")
                self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        # TODO: START
        # send temperature to the cloud service with regular intervals
        while True:
            with self.lock:
             
                #hneter ut måleing, enhet og tidspunt fra simulatren
                value = float(self.measurement.value)
                unit = str(self.measurement.unit)
                timestamp = str(self.measurement.timestamp)
                
                # # Hardkodede testverdier
                # value = 25.0
                # unit = "C"
                # timestamp = "2025-05-27 12:00:00"
                
                url = common.BASE_URL + f"device/{self.did}/current"
                #bygger opp JSON datoen som skal sendes til cloud service
                data = {
                    "newValue": value,
                    "newSensorUnit": unit,
                    "newTimestamp": timestamp
                }
                
                try:
                    response = requests.post(url, json=data)  # send HTTP Post request to cloud service
                    response.raise_for_status()  # check for HTTP errors
                    logging.info(f"Nye målinger sendt til cloud service: {data}")            
                except requests.RequestException as e:
                    logging.error(f"Feil ved sending av målinger til cloud service: {e}")
                    
                time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)  # wait for a given time before next request
            
        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):

        # TODO: START
        
        # create and start thread simulating physical temperature sensor
        simulator_thread = threading.Thread(target=self.simulator)
        simulator_thread.start()
        
        # create and start thread sending temperature to the cloud service
        client_thread = threading.Thread(target=self.client)
        client_thread.start()

        # # Hold hovedtråden i live (ellers avsluttes programmet)
        simulator_thread.join()
        client_thread.join()

        # TODO: END
        
 
#må ha denne her for å kjøre scriptet direkte via terminal       
if __name__ == "__main__":
    sensor = Sensor(common.TEMPERATURE_SENSOR_DID)
    sensor.run()

