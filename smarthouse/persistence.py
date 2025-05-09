import sqlite3 #import av sqlite3 bibliotek
from typing import Optional
from smarthouse.domain import (
    Measurement,
    SmartHouse,
    Sensor,
    Actuator,
    MIXActuatorSensor,
    Room,
    Floor,
)
class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False) #her dannes koblingen til databasen

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        # TODO: START here! remove the following stub implementation and implement this function 
        #       by retrieving the data from the database via SQL `SELECT` statements.
        
        #okei, så vi må lage en ny smarthus instans og så hente ut dataene fra databasen
        # og så lage et nytt smarthus objekt med de dataene vi har hentet ut
        # og så returnere det nye smarthus objektet
        dummySmarthus = SmartHouse() # oppretter et tomt smarthus
        lokalCursor = self.cursor()
        
        # #utfører nå SQL-spørringen for å hente ut all nødvenig informasjon fra databasen
        # #hneter ut alle etasjene
        
        
        # #danner etasjer
        # #så fra room tabellen ser vi at floor er definert. Lager derfor en liste med etasjer
        lokalCursor.execute('SELECT DISTINCT floor FROM rooms ORDER BY floor') #teller alle etasjer ( det blir 2 stk)
        floor_map = {}  # Map floor numbers to Floor objects
        room_map = {}  # Map room IDs to Room objects
        etasjerader = lokalCursor.fetchall() #henter alle etasjene som er distinkte, forid jeg kan ikke anta det er stignede eller sekvensielt uten hull
        for etajerad in etasjerader:
            etasjenummer = etajerad[0]
            NewFloor = dummySmarthus.register_floor(etasjenummer) #danner etasje ved bruk av smarthus klasen og legger til her
            floor_map[etasjenummer] = NewFloor  # Store the Floor object in the map
            #dummyFloors.append(NewFloor) #legger etasjen til i listen over etasjer
        
        lokalCursor.execute('SELECT * FROM rooms') # jeg skal ha id:int, floor(altså klassen), area:int , og name:string
        alleRommene = lokalCursor.fetchall() #HENTER ALLE ROMMENE 
        for rom in alleRommene:
            rom_id = rom[0] #iden til rommet
            etasje = rom[1] #etasje nummeret til rommet
            areal = rom[2] #arealet til rommet
            navn = rom[3] #navnet til rommet, feks kjøkken
                    
             
            if etasje not in floor_map:
                raise ValueError(f"Etasjenummer {etasje} finnes ikke i floor_map!")

            riktigEtasjeObj = floor_map[etasje]  # ← Denne linja MÅ til!
            
            #oppretter rom på ''normal'' måte type delA først uten ID
            nyttRom = dummySmarthus.register_room(riktigEtasjeObj, areal, navn) #danner rommet ved bruk av smarthus klasen som vanlig
            nyttRom.set_id(rom_id) #tilegner rommet IDen fra databasen
            romnummer = rom[0]
            room_map[romnummer] = nyttRom  # Store the Room object in the map
        
        
        
        # #henter ut alle enheter fra databasen, der jeg kan brukene JOIN for ''Devices.room'' ilag med ''Rooms.id''
        # #for å få ut alle enhetene med tilhørende rom og etasje
        # #bruker nå join for å danne en ny virtuell tabell i SQL der jeg henter ut alle enheter med tilhørende rom og etasje            
        
        #smart_lock = Actuator(id="4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", supplier="MythicalTech", model_name="Guardian Lock 7000", device_type='smart lock')
        # Register devices in rooms
        #DEMO_HOUSE.register_device(garage, automatic_garage_door)
        
        #def __init__(self, id: str, supplier: str, model_name: str, device_type:str,  sensor_unit: str):
        #super().__init__(id, supplier, model_name,device_type) 
        #self.sensor_unit = sensor_unit  #her defineres målenehten til sensoren.
       
       
    #    CO2_sensor = Sensor(id="8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", supplier="ElysianTech", model_name="Smoke Warden 1000", device_type='co2sensor', sensor_unit='ppm')
    #  light_bulb = Actuator(id="6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", supplier="Elysian Tech", model_name="Lumina Glow 4000", device_type='Light Bulp')
        
        lokalCursor.execute('SELECT d.id, d.supplier, d.product, d.kind, m.unit, d.category, d.room, d.state FROM devices d FULL OUTER JOIN measurements m ON d.id =m.device GROUP by id;') #--primær nøkkel er id, trenger bare en linje per sensoer/aktuator enhet                           
        alleEnheter = lokalCursor.fetchall() #henter ut alle enhetene fra databasen 'device' og matcher under ' measurements' for å hente ut relevant målenhet
        #bruker full outer join for å få med alle enheter selv om de ikke har units... da blir det NULL 
        for enhet in alleEnheter:
            enhet_id = enhet[0] #IDen til enheten, feks 4d51 osv
            supplier = enhet[1]
            model_name = enhet[2]
            device_type = enhet[3] 
            sensor_unit = enhet [4] #kan være NULL
            SensorORActuator = enhet[5] #sensor eller aktuator
            rommetDenSkalI= enhet[6] #rommet den skal i, feks kjøkken
            
            #TODO ved oppstart finnes ikke enhet[7], denne kommer først under update_actuator_state.. må finne en mer robost løsning. 
            state = enhet[7] #sier noe om tilstanden, hvis aktuator, så er det null, 0 eller 1 eller float
            
            riktigRomObj = room_map[rommetDenSkalI]  # ← Denne linja MÅ til!
            #DEMO_HOUSE.register_device(living_room, CO2_sensor)
            #hvis enhet er en sensor.. lag sensor... 
            if SensorORActuator == ('sensor'):
                #air_quality_sensor = Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "CelestialSense Technologies", "AeroGuard Pro", 'luftkvalitetsensor', '%-kvalitet')
                nySensor = Sensor(enhet[0],enhet[1],enhet[2],enhet[3], enhet[4]) #danner sensor ved bruk av smarthus klasen og legger til her
                dummySmarthus.register_device(riktigRomObj, nySensor) #her registreres sensorene i rommet
                
            if SensorORActuator == ('actuator'):
                # light_bulb = Actuator(id="6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", supplier="Elysian Tech", model_name="Lumina Glow 4000", device_type='Light Bulp')
                nyActuator = Actuator(enhet[0],enhet[1],enhet[2],enhet[3]) #danner actuator ved bruk av smarthus klasen og legger til her
                if state is not None:
                    if state == 0:
                        nyActuator.turn_off() #hvis state er 0, så slår jeg av aktuatoren
                    elif state == 1:
                        nyActuator.turn_on()
                    elif state > 1:
                        nyActuator.turn_on(state)  #hvis state er større enn 1, så slår jeg på aktuatoren med en float verdi                    
                    
                dummySmarthus.register_device(riktigRomObj, nyActuator) #her registreres aktuatoren i rommet

                
          
        lokalCursor.close()
        # return dummySmarthus
        return dummySmarthus


    def add_sensor_measurement_and_save(self, sensorID: str, timestamp:str, value:float, unit:str):
        lokalCursor = self.conn.cursor()
        queryReg = 'INSERT INTO measurements (device, ts, value, unit) VALUES (?, ?, ?, ?)'
        lokalCursor.execute(queryReg, (sensorID, timestamp, value, unit))
        self.conn.commit()  # Commit the changes
        lokalCursor.close()
    
    def delete_oldest_measurements_and_save(self, sensor: Sensor):
        sensorID = sensor.id
        lokalCursor = self.conn.cursor()
        queryReg = 'DELETE FROM measurements WHERE device = ? AND ts = (SELECT ts FROM measurements WHERE device = ? ORDER BY ts ASC LIMIT 1);'
        
        lokalCursor.execute(queryReg, (sensorID, sensorID))
        rowsAffected= lokalCursor.rowcount
        self.conn.commit()  # Commit the changes
        lokalCursor.close()            
        return rowsAffected
     
    def get_all_sensor_readings(self,sensorID: str):
        lokalCursor = self.conn.cursor()
        query_reg = 'SELECT device, ts, value, unit from measurements m WHERE m.device = ? ORDER BY ts DESC'        
        lokalCursor.execute(query_reg, (sensorID,))
        resultat = lokalCursor.fetchall() #henter ut alt
        lokalCursor.close()
        return resultat
        
            
    
    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        # """
        # Retrieves the most recent sensor reading for the given sensor if available.
        # Returns None if the given object has no sensor readings.
        # """
        
        # LAFO pga del C ønsker jeg å kunne sende denne funksjonen både ID og sensorinstans, trenger bare iden
        if isinstance(sensor, Sensor):
            IdLokal = sensor.id  
        elif isinstance(sensor, str): #for del C, sender bare iden som string
            IdLokal = sensor
        else:
            return None  # Invalid input type
        
        lokalCursor = self.conn.cursor()        
        query_reg = 'SELECT m.device, m.ts, m.value, m.unit FROM measurements m WHERE m.device = ? ORDER BY ts DESC LIMIT 1'
        lokalCursor.execute(query_reg, (IdLokal,)) 
        result = lokalCursor.fetchone() 
    
        if result is None:
            lokalCursor.close()  # Close the cursor before returning
            return None  # No measurements found
    
         # Create a Measurement object
        measurement = Measurement(timestamp=result[1], value=result[2], unit=result[3])  #[0 ]er device
        lokalCursor.close()
        return measurement
    
    def read_actuator_state(self, actuator_id) -> int: #LAFO lagt til for del C
        # actuator_id =  #iden to actuator which state is to be read
        curs = self.cursor()
        queryReqB = ('SELECT d.id, d.category, d.state from devices d WHERE d.id = ?')         
        curs.execute(queryReqB, (actuator_id,)) #placeholder igjen for å unngå SQL-injection.. MERK , bak actuator id for å sende som tuple, hvis ikke deler SQLIte den opp i antall tegn...
        results = curs.fetchall()
        # Close the connection
        curs.close()
        if results[0][1] == 'actuator':
          return results[0][2]
        return None

    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.
        
        actuator_id = actuator.id #iden til aktuatoren som skal få oppdater tilstand i databasen
        actuator_state = actuator.state #null, true eller fale eller en float
        
        curs = self.cursor()
        
        #FORUTSETTER AT JEG HAR NÅ EN STATE KOLONNE I DEVICES TABELLEN - SETTER INN DENNE KOLENNE HVIS DEN IKKE FINNES
        curs.execute('PRAGMA table_info(devices);') #henter ut informasjon om tabellen devices
        columns = [column[1] for column in curs.fetchall()] #henter ut kolonnene i tabellen devices
        #colums vil altså være id room kind supplier product state osv... 
        if 'state' not in columns: #hvis state ikke finnes i kolonnene, så må jeg lage den
            curs.execute('ALTER TABLE devices ADD COLUMN state FLOAT;') #utvider devices tabellen med en ny kolonne for å lagre tilstanden til aktuatoren. Gjøres bare første gangen
        
        #oppdaterer tilstanden til aktuatoren i databasen
        
        #må sjekke om det er en bool eller en float som er verdier, ser at uten dette så blir oven sin state 24(som er sp-punktet)
        #tenker løsningen er å sette alt til en int verdier uansett.. 0 hvis false, 1 hvis true eller over 1
        if isinstance(actuator_state, bool):
            actuator_state = int(actuator_state)  
            if actuator_state > 0:
                actuator_state = 1
            else:
                actuator_state = 0 
        elif isinstance(actuator_state, (int, float)) and actuator_state > 0:
            actuator_state = 1
        else:
            actuator_state = 0
    
        
        
        queryReqB = 'UPDATE devices SET state = ? WHERE id = ?' #endre så tilstanden der ID er funnet.         
        curs.execute(queryReqB, (actuator_state, actuator_id)) #placeholder igjen for å unngå SQL-injection..

        # Commit the changes
        self.conn.commit()
        
        # Close the connection
        curs.close()
        

    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        #SÅ OPPSUMERT... SAMLE ALLE MÅLINGENE FRA ENHETENE I ROMMET ETTER where romnavn', der unit = celsius... så del opp i datoer og finn gjennomsnittet for hver dato
        
        room_name = room.room_name #
        StartDate = from_date
        StopDate = until_date
        
        #rommet kan ha flere sensorer og aktuatorer med temp, så tar derfor å henter ut alle målingene for rommet
        #dette gjøres ved å bruke JOIN for å hente ut alle målingene for rommet
        curs = self.cursor()
        
        
        
        
        
        query = """
        SELECT STRFTIME('%F',m.ts) as eachDay, AVG(m.value) AS snittValueUtvalg, m.unit, d.room, r.id, r.name
        FROM measurements m
        LEFT JOIN devices d ON m.device = d.id
        LEFT JOIN rooms r ON d.room = r.id
        WHERE (date(ts) >= ? OR ? IS NULL)  -- Henter alt fra og med from_date hvis den er spesifisert
        AND (date(ts) <= ? OR ? IS NULL)  -- Henter alt til og med to_date hvis den er spesifisert
        AND unit ='°C'
        AND name = ? 
        GROUP BY eachDay
        ORDER BY eachDay
        ;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (StartDate,StartDate,StopDate,StopDate,room_name))  # Parameterisering
        results = cursor.fetchall()
        cursor.close()

        # Bygg ordboken med datoer og gjennomsnittstemperaturer
        daily_avg_temperatures={}
         
        for row in results:
            Wholedag = row[0] #henter ut døgns dato
            snittValue = round(row[1],4) #henter ut snittverdien for den dagen LAFO runder av til 4 decimaler ettersom testprogrammet har 4 desimaler.
        #fyller ordboken med dato og verdi
            daily_avg_temperatures[Wholedag] = snittValue #fyller ordboken med dato og verdi
        
        return daily_avg_temperatures
        
        
        
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        return NotImplemented

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        får inn rommets id/evt navn, og dato i formaet  2024-01-27...
        så må først hente ut rommet fra databasen, og så hente ut alle målingene for det rommet, så finne alle målingene den dagen, så finne average for hele døgnet, så se hvilke timer som overgår average med 4 målepunkter eller mer.
        """
        # TODO: implement
        
        room_name = room.room_name #iden til aktuatoren som skal få oppdater tilstand i databasen, denne iden er feks 1,2,3,4 osv..
        
        date_id = date #null, true eller fale eller en float
        curs = self.cursor()
        
        #må først finne iden til rommet
        curs.execute('SELECT d.id, d.room, r.id, r.name FROM devices d LEFT JOIN rooms r ON d.room = r.id WHERE r.name = ?', (room_name,)) #henter ut rommet med iden room_id
        ResultatQerA = curs.fetchall()
        sensor_ID = ResultatQerA[0][0] #henter iden til sensoren i romemt
        rom_ID = ResultatQerA[0][1] #henter ut iden til rommet
    
        
        
        queryReq = """
        -- Snitt per time
        WITH hourly_avg AS (  -- Korrekt navn på CTE
        SELECT strftime('%H', m.ts) AS hour, AVG(m.value) AS avgValueHourly
        FROM devices d
        LEFT JOIN measurements m ON m.device = d.id
        WHERE m.unit = '%' AND d.room = ? AND date(m.ts) = ?  -- Filtrering for rom og dato
        GROUP BY hour ),
        daily_avg AS (
        SELECT AVG(avgValueHourly) AS avgValueDaily
        FROM hourly_avg  -- Korrekt referanse til CTE
        )
        -- Hent timer med 3 eller flere målinger over det daglige gjennomsnittet
        SELECT hourly_avg.hour, COUNT(m.value) AS count_above_avg
        FROM measurements m
        JOIN hourly_avg ON strftime('%H', m.ts) = hourly_avg.hour  -- Korrekt referanse til CTE
        JOIN daily_avg ON 1=1  -- Dummy join for å få tilgang til avgValueDaily
        WHERE date(m.ts) = ? 
            AND m.device = ?
            AND m.value > daily_avg.avgValueDaily  -- Korrekt referanse til CTE
        GROUP BY hourly_avg.hour  -- Korrekt referanse til CTE
        HAVING COUNT(m.value) >= 4;  -- Minimum 4 målinger over gjennomsnittet
        """ 
        
        curs.execute(queryReq,(rom_ID,date_id,date_id,sensor_ID)) #placeholder igjen for å unngå SQL-injection..
        resultatOfReg = curs.fetchall() #henter ut resultatet av spørringen
        #vet nå at ofrmaleter er HOUR/tellinger over... der vi skal ha HOUR som feks er row[0] for hver linje
        
        resultListe = [] #lager en liste for å lagre resultatene
        for row in resultatOfReg:
            resultListe.append(int(row[0]))
        #returnerer listen med timer som har mer enn 3 målinger over average
        # Close the connection
        
        
        curs.close()
        return resultListe

