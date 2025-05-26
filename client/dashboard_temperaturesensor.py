import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common

#denne delen av koden er for å håndtere temperaturmåleren i dashbordet
# den er ment å sende en HTTP GET request til cloud service for å hente gjeldende temperatur
# og oppdatere brukergrensesnittet med den nye temperaturen

def refresh_btn_cmd(temp_widget, did):

    logging.info("Temperature refresh")

    # # TODO: START
    # # send request to cloud service to obtain current temperature

    # # # replace statement below with measurement from response
    # # sensor_measurement = SensorMeasurement(init_value="-273.15")

    url = common.BASE_URL + f"device/{did}/current"  # URL for fetching current temperature
    response = requests.get(url)  # send HTTP GET request to cloud service for å hente gjeldende temperatur
    data = response.json() #vet fra del C at dataen er i JSON
    # parse the JSON response                 
    verdi = data.get('value', "-273.15.. finner ikke en tabell-kolonne med navn value") #bruker get funksjon til list(returverdi).
    #enten får jeg match med nøkkelen 'value' som samsvarer med tabell(device, ts, value 
    # eller unit er mulig), og hvis ikke default -273.15
    
    sensor_measurement = SensorMeasurement(verdi)  #lager et SensorMeasurement objekt med verdien fra cloud service
    #jeg kan alterantiv bruke sensor_measurement = SensorMeasurement(init_value=verdi) for å opprette et nytt objekt
   
    # TODO: END

    # update the text field in the user interface
    temp_widget['state'] = 'normal' # to allow text to be changed
    temp_widget.delete(1.0, 'end')
    temp_widget.insert(1.0, sensor_measurement.value)
    temp_widget['state'] = 'disabled'


def init_temperature_sensor(container, did):

    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')

    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'

    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))

    refresh_button.grid(column=1, row=0, padx=20, pady=20)
