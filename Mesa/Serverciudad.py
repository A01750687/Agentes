import mesa
from CIudad import *  # Importa las clases y el modelo que definiste en CIudad.py

# Configuración de visualización
def agent_portrayal(agent):
    if isinstance(agent, Car):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 1,
            "Color": "blue",
            "r": 0.5
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
    elif isinstance(agent, Park):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "yellow",
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
    elif isinstance(agent, Calle):
        # Flechas naranjas para indicar la dirección de la calle
        portrayal = {
            "Shape": "arrowHead",
            "Filled": "true",
            "Layer": 0,
            "Color": "orange",
            "scale": 0.5,
            "heading_x": 0.0,
            "heading_y": 1.0,
        }
        if agent.direccion == "E":
            portrayal["heading_x"] = 1.0
            portrayal["heading_y"] = 0.0
        elif agent.direccion == "O":
            portrayal["heading_x"] = -1.0
            portrayal["heading_y"] = 0.0
        elif agent.direccion == "N":
            portrayal["heading_x"] = 0.0
            portrayal["heading_y"] = -1.0
        elif agent.direccion == "S":
            portrayal["heading_x"] = 0.0
            portrayal["heading_y"] = 1.0
    return portrayal

# Parámetros del modelo
num_cars = 3  # Número de autos en el modelo
width = 24  # Ancho de la cuadrícula
height = 24  # Alto de la cuadrícula

# Configuración de la cuadrícula de visualización
grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    width,
    height,
    500,
    500
)

# Configuración del servidor para visualizar el modelo
server = mesa.visualization.ModularServer(
    CityModel,  # Clase del modelo
    [grid],  # Visualización de la cuadrícula
    "City Model",  # Título de la ventana
    {"num_cars": num_cars, "width": width, "height": height}  # Parámetros del modelo
)

server.port = 853  
server.launch()
