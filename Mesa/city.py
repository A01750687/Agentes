from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import math

class build(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass  

class Semaforo(Agent):
    def __init__(self, unique_id, model, estado_inicial="verde"):
        super().__init__(unique_id, model)
        self.estado = estado_inicial  # El semáforo empieza en el estado especificado ("rojo" o "verde")
        self.step_count = 0

    def step(self):
        # Incrementar el contador en cada paso
        self.step_count += 1
        
        # Cambiar de color cada 10 pasos
        if self.step_count >= 10:
            self.estado = "rojo" if self.estado == "verde" else "verde"
            self.step_count = 0  # Reiniciar el contador


class park(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass

class car(Agent):
    def __init__(self, unique_id, model,streets,start_park,end_park):
        super().__init__(unique_id, model)
        # Rutas
        self.Upstreets = streets['up']
        self.Downstreets = streets['down']
        self.Lstreets = streets['left']
        self.Rstreets = streets['right']
        # Inicio y destino
        self.start_park = start_park  # Estacionamiento inicial
        self.destination = end_park  

        self.prevpos = self.pos

    def step(self):
        
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # No permite posicionarse sobre build y car
        valid_positions = [
            pos for pos in possible 
            if all(not isinstance(agent, build) and not isinstance(agent,car) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]
        
        # Checa su posición para saber a que dirección ir
        if self.pos in self.Upstreets:
            # No permite ir abajo
            valid_positions = [pos for pos in valid_positions if pos[1] >= self.pos[1]]
        if self.pos in self.Downstreets:
            # No permite ir arriba
            valid_positions = [pos for pos in valid_positions if pos[1] <= self.pos[1]]
        if self.pos in self.Lstreets:
            # No permite ir a la derecha
            valid_positions = [pos for pos in valid_positions if pos[0] <= self.pos[0]]
        if self.pos in self.Rstreets:
            # No permite ir a la izquierda
            valid_positions = [pos for pos in valid_positions if pos[0] >= self.pos[0]]

        semaforo = None

        # Obtiene todos los contenidos de la posición actual
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        # Busca si hay un objeto de la clase Semaforo en la posición actual
        for item in cell_contents:
            if isinstance(item, Semaforo):
                semaforo = item

        valid_positions = [
            pos for pos in valid_positions 
            if all(
                not (isinstance(agent, park) and pos != self.destination) 
                for agent in self.model.grid.get_cell_list_contents([pos])
            )
        ]

        print(self.destination)

        if valid_positions:
            if semaforo and (semaforo.estado == "rojo"):
                self.model.grid.move_agent(self, self.pos)
            else:
                # Selecciona la posición más cercana a self.destination
                new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))

                # Si la nueva posición es igual a prevpos, intenta otra posición
                if new_position == self.prevpos and len(valid_positions) > 1:
                    valid_positions.remove(new_position)
                    new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))
    
                # Actualiza prevpos y mueve el agente
                self.prevpos = self.pos
                self.model.grid.move_agent(self, new_position)
        else:
            self.prevpos = self.pos
            self.model.grid.move_agent(self, self.pos)
    
class cityModel(Model):
    def __init__(self, N, w, h):
        self.num_agents = N
        self.grid = MultiGrid(w, h, False)
        self.schedule = RandomActivation(self)

        streets = {}
        streets['up'] = []
        streets['down'] = []
        streets['left'] = []
        streets['right'] = []
        
        # Crear y colocar <- left streets
        for x in range(1,13):
            for y in range(10,12):
                streets['left'].append((x,y))
        for x in range(15,22):
            for y in range(10,12):
                streets['left'].append((x,y))
        for x in range(1,23):
            for y in range(22,24):
                streets['left'].append((x,y))
        for x in range(1,6):
            for y in range(17,19):
                streets['left'].append((x,y))
        for x in range(15,22):
            for y in range(4,6):
                streets['left'].append((x,y))
        
        for x in range(11,16):
            y = 11
            streets['left'].append((x,y))
        for y in range(12,22):
            x = 13
            streets['left'].append((x,y))
        for y in range(2,8):
            x = 13
            streets['left'].append((x,y))

        # Crear y colocar ^ up streets
        for x in range(14,16):
            for y in range(12,23):
                streets['up'].append((x,y))
        for x in range(14,16):
            for y in range(2,9):
                streets['up'].append((x,y))
        for x in range(18,20):
            for y in range(18,23):
                streets['up'].append((x,y))
        for x in range(22,24):
            for y in range(0,24):
                streets['up'].append((x,y))
        for y in range(8,12):
            streets['up'].append((15,y))

        for x in range(2,12):
            y = 10
            streets['up'].append((x,y))

        for x in range(16,22):
            y = 10
            streets['up'].append((x,y))

        # Crear y colocar down streets
        for x in range(12,14):
            for y in range(12,22):
                streets['down'].append((x,y))
        for x in range(6,8):
            for y in range(11,22):
                streets['down'].append((x,y))
        for x in range(0,2):
            for y in range(0,24):
                streets['down'].append((x,y))
        for x in range(12,14):
            for y in range(1,8):
                streets['down'].append((x,y))
        for x in range(18,20):
            for y in range(1,8):
                streets['down'].append((x,y))
        
        for y in range(8,12):
            x = 12
            streets['down'].append((x,y))
        for x in range(2,12):
            y = 9
            streets['down'].append((x,y))
        for x in range(16,22):
            y = 9
            streets['down'].append((x,y))

        # Crear y colocar -> right streets
        for x in range(2,13):
            for y in range(8,10):
                streets['right'].append((x,y))
        for x in range(15,23):
            for y in range(8,10):
                streets['right'].append((x,y))
        for x in range(2,13):
            for y in range(4,6):
                streets['right'].append((x,y))
        for x in range(1,23):
            for y in range(0,2):
                streets['right'].append((x,y))
        for x in range(16,23):
            for y in range(16,18):
                streets['right'].append((x,y))
        for x in range(12,16):
            y = 8
            streets['right'].append((x,y))
        for y in range(12,22):
            x = 14
            streets['right'].append((x,y))
        for y in range(2,8):
            x = 14
            streets['right'].append((x,y))

        # Crear y colocar agentes `car`
        car_pairs = [
            ((2, 15), (21, 3)), 
            ((3, 6), (20, 15)),
            ((4, 19), (20, 18)), 
            ((4, 12), (17, 6)),
            ((4, 3), (17, 6)), 
            ((8, 14), (21, 3)),
            ((9, 21), (11, 17)), 
            ((9, 2), (11, 17))
        ]
        i = 0
        for start, end in car_pairs:
            c = car(i, self, streets,start, end)
            self.schedule.add(c)
            self.grid.place_agent(c, start)
            i += 1
        
        # c = car(1,self,streets,car_pairs[0][0],car_pairs[0][1])
        # self.schedule.add(c)
        # self.grid.place_agent(c, car_pairs[0][0])

        unique_id = self.num_agents
        
        # Crear y colocar agentes `build` y `park`
        for i in range(2, 12):
            for j in range(2, 4):
                if ((i == 9 and j == 2) or (i == 4 and j == 3)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(2, 12):
            for j in range(6, 8):
                if ((i == 3 and j == 6) or (i == 10 and j == 7)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(13, 15):
            for j in range(9, 11):
                b = build(unique_id, self)
                self.schedule.add(b)
                self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(2, 6):
            for j in range(12, 17):
                if ((i == 4 and j == 12) or (i == 2 and j == 15)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(2, 6):
            for j in range(19, 22):
                if ((i == 4 and j == 19)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(8, 12):
            for j in range(12, 22):
                if ((i == 10 and j == 12) or (i == 8 and j == 14) or (i == 11 and j == 17) or (i == 9 and j == 21)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
        
        for i in range(16, 18):
            for j in range(2, 4):
                b = build(unique_id, self)
                self.schedule.add(b)
                self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(20, 22):
            for j in range(2, 4):
                if (i == 21 and j == 3):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(16, 18):
            for j in range(6, 8):
                if (i == 17 and j == 6):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(20, 22):
            for j in range(6, 8):
                b = build(unique_id, self)
                self.schedule.add(b)
                self.grid.place_agent(b, (i, j))
                unique_id += 1
        
        for i in range(16, 22):
            for j in range(12, 16):
                if ((i == 18 and j == 12) or (i == 20 and j == 15)):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(16, 18):
            for j in range(18, 22):
                if (i == 17 and j == 21):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
                
        for i in range(20, 22):
            for j in range(18, 22):
                if (i == 20 and j == 18):
                    p = park(unique_id, self)
                    self.schedule.add(p)
                    self.grid.place_agent(p, (i, j))
                else:
                    b = build(unique_id, self)
                    self.schedule.add(b)
                    self.grid.place_agent(b, (i, j))
                unique_id += 1
        # Posicionamiento semaforo
        semaforo_positions = [
                ((11, 4), "rojo"), ((11, 5), "rojo"), ((12, 6), "verde"), ((13, 6), "verde"),
                ((18, 6), "verde"), ((19, 6), "verde"), ((20, 5), "rojo"), ((20, 4), "rojo"),
                ((22, 15), "verde"), ((23, 15), "verde"), ((21, 16), "rojo"), ((21, 17), "rojo"),
                ((20, 22), "rojo"), ((20, 23), "rojo"), ((19, 21), "verde"), ((18, 21), "verde"),
                ((0, 19), "verde"), ((1, 19), "verde"), ((2, 18), "rojo"), ((2, 17), "rojo")
            ]
        for pos, estado_inicial in semaforo_positions:
                semaforo = Semaforo(unique_id, self, estado_inicial)
                self.schedule.add(semaforo)
                self.grid.place_agent(semaforo, pos)
                unique_id += 1

    def step(self):
        self.schedule.step()
