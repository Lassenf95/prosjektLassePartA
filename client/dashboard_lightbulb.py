import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common

#denne delen av koden er for å håndtere lyspæren i dashbordet
# den er ment å sende en HTTP PUT request til cloud service med ny tilstand for lyspæren


def fetch_lightbulb_state(did):
    url = common.BASE_URL + f"actuator/{did}/current"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"API-respons for lyspære: {data}")  # <-- Legg til denne
        return 'On' if data.get('state', 0) else 'Off'
    except Exception as e:
        logging.error(f"Feil ved henting av lyspærestatus: {e}")
        return 'Off'

def poll_lightbulb_state(lightbulb_state_var, did, container):
    state = fetch_lightbulb_state(did)
    lightbulb_state_var.set(state)
    container.after(1000, poll_lightbulb_state, lightbulb_state_var, did, container)


def lightbulb_cmd(state, did):

    new_state = state.get()

    logging.info(f"Dashboard: {new_state}")

    # TODO: START
    # send HTTP request with new actuator state to cloud service
   
    state_value = 1 if new_state == 'On' else 0 #henter tilstand som skal sendes til cloud service
    url = common.BASE_URL + f"device/{did}" #URLEn som blir benyttet for å sende til cloud service
    
    passingParamter = {"stateNewValid": state_value} #dette er det som skal sendes til cloud service
    requests.put(url, json=passingParamter) #sender en HTTP PUT request til cloud service med ny tilstand
    #ELLER DIREKTE SLIK.
    #VIKTIG Å HUSKE at data som sendes til cloud service må være i JSON format, og input er en dictionary
    #requests.put(url, json={"stateNewValid": state_value}) #sender en HTTP PUT request til cloud service med ny tilstand    
    #som man ser i dokumentasjon for REST_apiet i swagger er {"stateNewValid": 1} for On og {"stateNewValid": 0} for Off
    #for forståelse er dette akkurat det som som bruno gjør mot api.py i smarthouse prosjektet bare nå via skytjenesten
    
    #TRY CATCH EXECEPTION UNDER FOR MERE ROBUSTHET(HENTET FRA CHATGPT)
    # try:
    #     # Send HTTP request med riktig JSON-body
    #     response = requests.put(url, json={"stateNewValid": state_value})
    #     response.raise_for_status()
    #     logging.info(f"Lampestatus oppdatert: {response.json()}")
    # except Exception as e:
    #     logging.error(f"Feil ved oppdatering av lyspære: {e}")      

    # send HTTP request with new actuator state to cloud service
    # TODO: END


def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
    
    # Legg til en label for å vise status
    status_label = ttk.Label(lb_lf, text="Status: Off")
    status_label.grid(column=0, row=1, columnspan=2, pady=(10, 0))

    # # Funksjon for å oppdatere status-label
    def update_status_label(*args):
        status_label.config(text=f"Status: {lightbulb_state_var.get()}")

    # # Koble label-oppdatering til endring av state
    lightbulb_state_var.trace_add("write", update_status_label)

    # # Start polling for status
    container.after(1000, poll_lightbulb_state, lightbulb_state_var, did, container)