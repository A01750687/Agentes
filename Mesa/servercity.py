import mesa
from city import *

def agent_portrayal(agent):
    if isinstance(agent, car):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5
        }
    elif isinstance(agent, build):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "black",
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Semaforo):
        color = "green" if agent.estado == "verde" else "red"
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": color,
            "w": 0.5,
            "h": 0.5
        }
    elif isinstance(agent, park):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "yellow",
            "w": 1,
            "h": 1
        }
    return portrayal


coches: int = 1
w: int = 24
h: int = 24

grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    w,
    h,
    500,
    500
) # 10x10 grid, 500x500 pixels

server = mesa.visualization.ModularServer(
    cityModel,
    [grid],
    "City Model",
    {"N": coches, "w": w, "h": h}
)

server.port = 8521
server.launch()
