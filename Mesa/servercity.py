import mesa
from city import *
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Modelo de Mesa
coches: int = 1
w: int = 33
h: int = 33

def agent_portrayal(agent):
    if isinstance(agent, Car):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5
        }
    else:
        # Otras representaciones omitidas para brevedad
        portrayal = {}
    return portrayal

grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    w,
    h,
    500,
    500
)

model = cityModel(N=coches, w=w, h=h)

# Ruta para enviar IDs y posiciones de agentes Car
@app.route('/get_car_positions', methods=['GET'])
def get_car_positions():
    car_data = [
        {"id": agent.unique_id, "x": agent.pos[0],"y":agent.pos[1]}
        for agent in model.schedule.agents if isinstance(agent, Car)
    ]
    model.step()
    return jsonify(car_data)

@app.route('/get_bus_positions', methods=['GET'])
def get_bus_positions():

    bus_data = [
        {"id": agent.unique_id, "x": agent.pos[0],"y":agent.pos[1]}
        for agent in model.schedule.agents if isinstance(agent, Bus)
    ]
    return jsonify(bus_data)

@app.route('/get_peatones_positions', methods=['GET'])
def get_peatones_positions():

    peaton_data = [
        {"id": agent.unique_id, "x": agent.pos[0],"y":agent.pos[1]}
        for agent in model.schedule.agents if isinstance(agent, Peaton)
    ]
    return jsonify(peaton_data)

@app.route('/get_ambulancia_positions', methods=['GET'])
def get_ambulancia_positions():

    ambulancia_data = [
        {"id": agent.unique_id, "x": agent.pos[0],"y":agent.pos[1]}
        for agent in model.schedule.agents if isinstance(agent, Ambulancia)
    ]
    return jsonify(ambulancia_data)

@app.route('/get_grua_positions', methods=['GET'])
def get_grua_positions():

    grua_data = [
        {"id": agent.unique_id, "x": agent.pos[0],"y":agent.pos[1]}
        for agent in model.schedule.agents if isinstance(agent, Grua)
    ]
    return jsonify(grua_data)

@app.route('/get_semaforos_state', methods=['GET'])
def get_semaforos_state():

    semaforo_data = [
        {"id": agent.unique_id, "state": 0 if agent.estado == "rojo" else 1}
        for agent in model.schedule.agents if isinstance(agent, Semaforo) and agent.unique_id % 2 == 0
    ]
    return jsonify(semaforo_data)

if __name__ == '__main__':
    # Corre Flask
    app.run(host='0.0.0.0', port=5000)  