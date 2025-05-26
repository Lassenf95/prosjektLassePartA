import logging
import threading
import time
import requests

from messaging import ActuatorState
import common

logging.basicConfig(level=logging.INFO)

class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')
        self.lock = threading.Lock()  # lock for å unngå race conditions. Må unngå å lese og skrive state samtidig

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:
            #LAFO alternativ lock, with self.lock: så slepper man åtenke på å låse og låse opp manuelt
            with self.lock:
                logging.info(f"Actuator {self.did}: {self.state.state}")
            #LAFO end
            #logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # TODO: START
        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response
        while True: #kjører i en uendelig løkke for å hente tilstand fra cloud service
            self.lock.acquire()  # låser for å unngå race conditions
            url = common.BASE_URL + f"device/{self.did}/current" #URLEn som blir benyttet for å sende til cloud service
            response=requests.get(url) #sender en HTTP GET request til cloud service for å hente gjeldende tilstand
            data = response.json()  # henter JSON data fra cloud service
            state_value = data.get('state', 0)  # bruker get funksjon for å hente state fra JSON dataen        
            #samme som før, dersom state ikke finnes i JSON dataen, default 0
            #bruker actuator state under messaging.py for å opprette et ActuatorState objekt
            self.state = ActuatorState(str(bool(state_value)))
            self.lock.release() # låser opp for at andre tråder kan lese og skrive state
            logging.info(f"Actuator {self.did} oppdatert til: {self.state.state}")
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)  # venter i en gitt tid før neste forespørsel
       
        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):
        
        # TODO: START

        # start thread simulating physical light bulb: NOTICE THREAD DEFINED ABOVE
        simulator_thread = threading.Thread(target=self.simulator)
        simulator_thread.start()
        
        # start thread receiving state from the cloud: NOTICE THREAD DEFINED ABOVE
        client_thread = threading.Thread(target=self.client)
        client_thread.start()

        #starter tråden for autotoggling hvert 10 sek
        toggler_thread = threading.Thread(target=self.toggler)
        toggler_thread.start()
        
        
        # # Hold hovedtråden i live (ellers avsluttes programmet)
        #OBS OBS join må alling være i samme rekkefølge som start, ellers kan det bli deadlock
        #og  tilleg må alle tråder startes med join samtidig, hvis ikke ikke ville de ikke kjøre parallet
        simulator_thread.join()
        client_thread.join()
        toggler_thread.join() 
        

        # TODO: END

    #LAFO START ønsker å  ha en toogler som skruer lyset av i 10 sek, så på i 10 sek, gjentakende
    #formålet er å sjekke at utsending fra flere steder funker
    def toggler(self):
        toggle = False
        while True:
            toggle = not toggle #ved neste iterasjon vil toggle være motsatt av forrige
            # Send ny state til API
            with self.lock:
                url = common.BASE_URL + f"device/{self.did}"
                data = {"stateNewValid": int(toggle)}
                try:
                    requests.put(url, json=data)
                    logging.info(f"Toggler: satte state til {toggle}")
                except Exception as e:
                    logging.error(f"Toggler-feil: {e}")
                time.sleep(10)


#må ha denne her for å kjøre scriptet direkte via terminal
if __name__ == "__main__":
    actuator = Actuator(common.LIGHTBULB_DID)
    actuator.run()