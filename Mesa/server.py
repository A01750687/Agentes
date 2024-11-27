import mesa
from city import *

def agent_portrayal(agent):
    if isinstance(agent, Car):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5
        }
    elif isinstance(agent, Bus):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "#9239e6",
            "r": 0.5
        }
    elif isinstance(agent, Ambulancia):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "#fa619c",
            "r": 0.5
        }
    elif isinstance(agent, Grua):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "#86ed77",
            "r": 0.5
        }
    elif isinstance(agent, Peaton):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "Orange",
            "r": 0.5
        }
    elif isinstance(agent, Cruce):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "purple",
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Build):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "black",
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Banqueta):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "#c9c9c9",
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Parada):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "#baf0f5",
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
    elif isinstance(agent, Rampa):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "#4a4848",
            "w": 1,
            "h": 1
        }
    elif isinstance(agent, Park):
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
w: int = 33
h: int = 33

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