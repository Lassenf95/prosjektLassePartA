import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
import os
def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }
    
class DeviceInfo(BaseModel):
    id: str
    model: str
    supplier: str
    device_type: str
    device_category: Literal["actuator"] | Literal["sensor"] | Literal["actuator_with_sensor"] | Literal["unknown"]
    room: int | None

# 



# # @app.get("/smarthouse/floor")   
# # def get_smarthouse_floor() -> dict[str, list]:
# #     """
# #     This endpoint returns an object that provides information
# #     about all the floors in the smarthouse.
# #     """ 
# #     # Get all floors in the smarthouse
# #     floors = smarthouse.get_floors()
     
# #     return  
     
#     # # Convert floors to a JSON-serializable format
#     # serialized_floors = [floor.to_dict() for floor in smarthouse.get_floors()]
#     # return {
#     #     "floors": serialized_floors
#     # }



# def get_smarthouse_floor(floor_number: int) -> dict[str, list]:
#     """
#     This endpoint returns information object the floor
#     """
#     floor = smarthouse.get_floor_by_number(floor_number)
# #    # If the floor does not exist, return a 404 error
# #     if not floor:
# #         return {"error": f"Floor {floor_number} not found"}

#     # # Serialize the floor information into a JSON-serializable format
#     # serialized_rooms = [room.to_dict() for room in floor.get_rooms()]
#     # return {
#     #     "floor_number": floor.number,
#     #     "total_area": floor.get_area(),
#     #     "rooms": serialized_rooms
#     # }
#     # ALTERNATIV BRUKE :https://fastapi.tiangolo.com/advanced/response-directly/ 
     
     

    
#     # ALTERNATIV BRUKE :https://fastapi.tiangolo.com/advanced/response-directly/
    
    
    
    

    
# @app.get("/smarthouse/floor") 
# def get_smarthouse_floor() -> dict[str, int | float]:
#     """
#     This endpoint returns an object that provides information
#     about on all the floors in the smarthouse
#     """
#     # return {
#     #     "no_rooms": len(smarthouse.get_rooms()),
#     #     "no_floors": len(smarthouse.get_floors()),
#     #     "registered_devices": len(smarthouse.get_devices()),
#     #     "area": smarthouse.get_area()
#     # }
#     return NotImplemented

# TODO: implement the remaining HTTP endpoints as requested in
# https://github.com/selabhvl/ing301-projectpartC-startcode?tab=readme-ov-file#oppgavebeskrivelse
# here ...


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


