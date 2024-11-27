from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import math

class Build(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass  

class Grua(Agent):
    def __init__(self, unique_id, model,streets,busStop):
        super().__init__(unique_id, model)
        # self.ocupado = True
        self.ocupado = False
        self.Upstreets = streets['up']
        self.Downstreets = streets['down']
        self.Lstreets = streets['left']
        self.Rstreets = streets['right']
        self.prevpos = self.pos
        self.busStop = busStop

        self.hospital = (23,23)

        self.destination = busStop[1]
        self.count = 1
    
    def ayuda(self):
        return self.pos

    def step(self):
        if not self.ocupado:
            if self.count + 1 > max(self.busStop.keys()):
                self.count = 0

            self.destination = self.busStop[self.count + 1]

        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # Filtrar posiciones válidas
        valid_positions = [
            pos for pos in possible 
            if all(not isinstance(agent, Grua) and not isinstance(agent, Ambulancia) and not isinstance(agent, Parada) and not isinstance(agent, Banqueta) and not isinstance(agent, Build) and not isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]

        # Filtrar según la dirección de las calles
        if self.pos in self.Upstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] >= self.pos[1]]
        if self.pos in self.Downstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] <= self.pos[1]]
        if self.pos in self.Lstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] <= self.pos[0]]
        if self.pos in self.Rstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] >= self.pos[0]]

        valid_positions = [
            pos for pos in valid_positions 
            if all(
                not (isinstance(agent, Park) and pos != self.destination) 
                for agent in self.model.grid.get_cell_list_contents([pos])
            )
        ]

        if valid_positions:
            new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))
            if new_position == self.prevpos and len(valid_positions) > 1:
                valid_positions.remove(new_position)
                new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))

            semaforo = None
            cell_contents = self.model.grid.get_cell_list_contents([new_position])

            for item in cell_contents:
                if isinstance(item, Semaforo):
                    semaforo = item

            if semaforo and (semaforo.estado == "rojo"):
                self.model.grid.move_agent(self, self.pos)
                new_position = self.pos

            # Verificar si estamos en la parada de destino
            if self.destination in possible:
                if self.ocupado:
                    if self.destination != self.hospital:
                        self.destination = self.hospital
                        cell_contents = self.model.grid.get_cell_list_contents([valid_positions])
                        for pos in cell_contents:
                            for item in pos:
                                if isinstance(item, Car) and item.pos == self.destination:
                                    item.delete = True
                    else:
                        self.destination = self.busStop[self.count]
                        self.ocupado = False
                else:
                    self.count += 1

            self.prevpos = self.pos
            self.model.grid.move_agent(self, new_position)
        else:
            self.prevpos = self.pos
            self.model.grid.move_agent(self, self.pos)

class Ambulancia(Agent):
    def __init__(self, unique_id, model,streets,busStop):
        super().__init__(unique_id, model)
        # self.ocupado = True
        self.ocupado = False
        self.Upstreets = streets['up']
        self.Downstreets = streets['down']
        self.Lstreets = streets['left']
        self.Rstreets = streets['right']
        self.prevpos = self.pos
        self.busStop = busStop

        self.hospital = (23,23)

        self.destination = busStop[1]
        self.count = 1
    
    def ayuda(self):
        return self.pos

    def step(self):
        if not self.ocupado:
            if self.count + 1 > max(self.busStop.keys()):
                self.count = 0

            self.destination = self.busStop[self.count + 1]

        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # Filtrar posiciones válidas
        valid_positions = [
            pos for pos in possible 
            if all(not isinstance(agent, Grua) and not isinstance(agent, Ambulancia) and not isinstance(agent, Parada) and not isinstance(agent, Banqueta) and not isinstance(agent, Build) and not isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]

        # Filtrar según la dirección de las calles
        if self.pos in self.Upstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] >= self.pos[1]]
        if self.pos in self.Downstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] <= self.pos[1]]
        if self.pos in self.Lstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] <= self.pos[0]]
        if self.pos in self.Rstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] >= self.pos[0]]

        valid_positions = [
            pos for pos in valid_positions 
            if all(
                not (isinstance(agent, Park) and pos != self.destination) 
                for agent in self.model.grid.get_cell_list_contents([pos])
            )
        ]

        if valid_positions:
            new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))
            if new_position == self.prevpos and len(valid_positions) > 1:
                valid_positions.remove(new_position)
                new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))

            semaforo = None
            cell_contents = self.model.grid.get_cell_list_contents([new_position])

            for item in cell_contents:
                if isinstance(item, Semaforo):
                    semaforo = item

            if semaforo and (semaforo.estado == "rojo"):
                self.model.grid.move_agent(self, self.pos)
                new_position = self.pos

            # Verificar si estamos en la parada de destino
            if self.destination in possible:
                if self.ocupado:
                    if self.destination != self.hospital:
                        self.destination = self.hospital
                        cell_contents = self.model.grid.get_cell_list_contents([valid_positions])
                        for pos in cell_contents:
                            for item in pos:
                                if isinstance(item, Peaton) and item.pos == self.destination:
                                    item.delete = True
                    else:
                        self.destination = self.busStop[self.count]
                        self.ocupado = False
                else:
                    self.count += 1

            self.prevpos = self.pos
            self.model.grid.move_agent(self, new_position)
        else:
            self.prevpos = self.pos
            self.model.grid.move_agent(self, self.pos)

class Cruce(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Peaton(Agent):
    def __init__(self, unique_id, model,ambulancias):
        super().__init__(unique_id, model)
        self.prevpos = None  # Almacena la posición anterior
        self.espera = False
        self.delete = False

        self.ambulancias = ambulancias

        self.choque = False
        
        # Tiempo para poder esperar el bus
        self.puedeEsperar = False
        self.count = 0

    def subir(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.delete = True

    def pedirAyuda(self):
        # Inicializar la variable para la ambulancia más cercana
        ambulancia_mas_cercana = None
        distancia_minima = float('inf')  # Comenzamos con una distancia infinita

        # Recorrer todas las ambulancias y calcular la distancia
        for ambulancia in self.ambulancias:
            posicion_ambulancia = ambulancia.ayuda()  # Suponiendo que 'ayuda()' devuelve la posición de la ambulancia
            
            # Calcular la distancia entre self.pos y la posición de la ambulancia
            distancia = self.calcular_distancia(self.pos, posicion_ambulancia)
            
            # Si encontramos una ambulancia más cercana, la actualizamos
            if distancia < distancia_minima:
                distancia_minima = distancia
                ambulancia_mas_cercana = ambulancia
        
        return ambulancia_mas_cercana

    def calcular_distancia(self, pos1, pos2):
        # Calcula la distancia euclidiana entre dos puntos
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def step(self):

        if self.choque:
            self.espera = True
            print("CHOQUE")
            ambulancia = self.pedirAyuda()
            ambulancia.ocupado = True
            ambulancia.destination = self.pos

        if self.count > 3:
            self.puedeEsperar = True

        if not self.puedeEsperar:
            self.count +=1

        if self.delete:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return
        # Obtener las posiciones vecinas
        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        # Filtrar posiciones válidas (solo Banqueta o Cruce)
        valid_positions = [
            pos for pos in possible
            if any(isinstance(agent, Banqueta) or isinstance(agent, Cruce) or isinstance(agent,Parada) or isinstance(agent,Rampa)  for agent in self.model.grid.get_cell_list_contents([pos]))
        ]

        # Funcion con Autobús
        parada = None
        peatonesParada = 0
        
        hayCoches = False

        # Obtiene todos los contenidos de la posición actual
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        # Busca si hay un objeto de la clase Semaforo en la posición actual
        for item in cell_contents:
            if isinstance(item, Parada):
                parada = item
            if isinstance(item, Peaton):
                peatonesParada+=1
            if isinstance(item, Car):
                self.choque = True
        
        self.espera = hayCoches

        # Filtrar la posición anterior
        if self.prevpos in valid_positions:
            valid_positions.remove(self.prevpos)

        for item in valid_positions:
            cell_contents = self.model.grid.get_cell_list_contents([item])
            semaforo = None
            for i in cell_contents:
                if isinstance(i, Semaforo):
                    semaforo = i
                if isinstance(i, Car):
                    self.espera = True
            if semaforo and (semaforo.estado == "verde"):
                valid_positions.remove(item)


        # Moverse a una posición válida aleatoria
        if valid_positions:
            new_position = random.choice(valid_positions)
            self.prevpos = self.pos  # Actualizar la posición anterior
            autobus = None
            posBus = None

            for pos in possible:
                cell_contents = self.model.grid.get_cell_list_contents([pos])
                for item in cell_contents:
                    if isinstance(item, Bus):
                        autobus = item
                        posBus = pos

            if parada and peatonesParada <= 2 and self.puedeEsperar:
                self.espera = True
                if autobus:
                    new_position = posBus
                    self.delete = True
            if self.espera:
                new_position = self.pos
            self.model.grid.move_agent(self, new_position)

class Banqueta(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)

class Rampa(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)

class Parada(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)

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


class Park(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass

class Bus(Agent):
    def __init__(self, unique_id, model,streets,busStop,ambulancias):
        super().__init__(unique_id, model)
        # Rutas
        self.Upstreets = streets['up']
        self.Downstreets = streets['down']
        self.Lstreets = streets['left']
        self.Rstreets = streets['right']
        self.prevpos = self.pos
        self.busStop = busStop

        self.ambulancias = ambulancias

        self.destination = busStop[1]
        self.count = 1
        self.timeCount = 0

        self.pasajeros = 0

    def step(self):
        if self.count + 1 > max(self.busStop.keys()):
            self.count = 0

        self.destination = self.busStop[self.count + 1]
        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # Filtrar posiciones válidas
        valid_positions = [
            pos for pos in possible 
            if all(not isinstance(agent, Grua) and not isinstance(agent, Ambulancia) and not isinstance(agent, Parada) and not isinstance(agent, Banqueta) and not isinstance(agent, Build) and not isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([pos]))
        ]

        # Filtrar según la dirección de las calles
        if self.pos in self.Upstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] >= self.pos[1]]
        if self.pos in self.Downstreets:
            valid_positions = [pos for pos in valid_positions if pos[1] <= self.pos[1]]
        if self.pos in self.Lstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] <= self.pos[0]]
        if self.pos in self.Rstreets:
            valid_positions = [pos for pos in valid_positions if pos[0] >= self.pos[0]]

        valid_positions = [
            pos for pos in valid_positions 
            if all(
                not (isinstance(agent, Park) and pos != self.destination) 
                for agent in self.model.grid.get_cell_list_contents([pos])
            )
        ]

        if valid_positions:
            new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))
            if new_position == self.prevpos and len(valid_positions) > 1:
                valid_positions.remove(new_position)
                new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))

            semaforo = None
            cell_contents = self.model.grid.get_cell_list_contents([new_position])
            selfpos_contents = self.model.grid.get_cell_list_contents([self.pos])

            for item in cell_contents:
                if isinstance(item, Semaforo):
                    semaforo = item

            if semaforo and (semaforo.estado == "rojo"):
                self.model.grid.move_agent(self, self.pos)
                new_position = self.pos

            # Verificar si estamos en la parada de destino
            if self.destination in possible and self.timeCount <= 3:
                self.model.grid.move_agent(self, self.pos)
                for item in selfpos_contents:
                    if isinstance(item, Peaton):
                        self.pasajeros += 1
                        item.delete = True  # Marca al peatón para eliminarlo
                new_position = self.pos
                self.timeCount += 1
                print(self.pasajeros)
                if self.timeCount == 3:
                    self.timeCount = 0
                    self.count += 1
                    for _ in range(random.randrange(0, 3)):
                        p = Peaton(self.model.agentsCount, self.model,self.ambulancias)
                        self.model.schedule.add(p)
                        self.model.grid.place_agent(p, self.busStop[self.count])
                        self.model.agentsCount+=1

            self.prevpos = self.pos
            self.model.grid.move_agent(self, new_position)
        else:
            self.prevpos = self.pos
            self.model.grid.move_agent(self, self.pos)

class Car(Agent):
    def __init__(self, unique_id, model,streets,start_park,end_park,parks,gruas):
        super().__init__(unique_id, model)
        # Rutas
        self.Upstreets = streets['up']
        self.Downstreets = streets['down']
        self.Lstreets = streets['left']
        self.Rstreets = streets['right']

        self.delete = False
        self.choque = False
        self.espera = False

        # Inicio y destino
        self.start_park = start_park  # Estacionamiento inicial
        self.destination = end_park  

        self.prevpos = self.pos
        self.parks = parks

        self.gruas = gruas

    def pedirAyuda(self):
        # Inicializar la variable para la ambulancia más cercana
        grua_mas_cercana = None
        distancia_minima = float('inf')  # Comenzamos con una distancia infinita

        # Recorrer todas las ambulancias y calcular la distancia
        for grua in self.gruas:
            posicion_grua = grua.ayuda()  # Suponiendo que 'ayuda()' devuelve la posición de la ambulancia
            
            # Calcular la distancia entre self.pos y la posición de la ambulancia
            distancia = self.calcular_distancia(self.pos, posicion_grua)
            
            # Si encontramos una ambulancia más cercana, la actualizamos
            if distancia < distancia_minima:
                distancia_minima = distancia
                grua_mas_cercana = grua
        
        return grua_mas_cercana

    def calcular_distancia(self, pos1, pos2):
        # Calcula la distancia euclidiana entre dos puntos
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def step(self):
        
        if self.choque:
            self.espera = True
            print("CHOQUE")
            grua = self.pedirAyuda()
            grua.ocupado = True
            grua.destination = self.pos

        if self.delete:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        possible = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # No permite posicionarse sobre build y car
        valid_positions = [
            pos for pos in possible 
            if all(not isinstance(agent, Peaton) and not isinstance(agent, Grua) and not isinstance(agent, Ambulancia) and not isinstance(agent, Parada) and not isinstance(agent, Banqueta) and not isinstance(agent, Build) and not isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([pos]))
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

        valid_positions = [
            pos for pos in valid_positions 
            if all(
                not (isinstance(agent, Park) and pos != self.destination) 
                for agent in self.model.grid.get_cell_list_contents([pos])
            )
        ]

        # Obtiene todos los contenidos de la posición actual
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        # Busca si hay un objeto de la clase Semaforo en la posición actual
        for item in cell_contents:
            if isinstance(item, Peaton):
                self.choque = True
                self.espera = True

        if valid_positions and not self.espera:
            # Selecciona la posición más cercana a self.destination
            new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))
            # Si la nueva posición es igual a prevpos, intenta otra posición
            if new_position == self.prevpos and len(valid_positions) > 1:
                valid_positions.remove(new_position)
                new_position = min(valid_positions, key=lambda pos: math.dist(pos, self.destination))

            semaforo = None

            # Obtiene todos los contenidos de la posición actual
            cell_contents = self.model.grid.get_cell_list_contents([new_position])

            # Busca si hay un objeto de la clase Semaforo en la posición actual
            for item in cell_contents:
                if isinstance(item, Semaforo):
                    semaforo = item

            if semaforo and (semaforo.estado == "rojo"):
                self.model.grid.move_agent(self, self.pos)
                new_position = self.pos

            # Actualiza prevpos y mueve el agente
            self.prevpos = self.pos
            self.model.grid.move_agent(self, new_position)
        else:
            self.prevpos = self.pos
            self.model.grid.move_agent(self, self.pos)
    
class cityModel(Model):
    def __init__(self, N, w, h):

        self.agentsCount = 0

        def building(self,pos,build_cells,parks,rampas,busStop,i):
            if pos in parks.values():
                b = Park(i,self)
                self.schedule.add(b)
                self.grid.place_agent(b,pos)
            elif pos in build_cells:
                b = Build(i,self)
                self.schedule.add(b)
                self.grid.place_agent(b,pos)
            elif pos in rampas:
                r = Rampa(i,self)
                self.schedule.add(r)
                self.grid.place_agent(r,pos)
            elif pos in busStop.values():
                bs = Parada(i,self)
                self.schedule.add(bs)
                self.grid.place_agent(bs,pos)
            else:
                b = Banqueta(i,self)
                self.schedule.add(b)
                self.grid.place_agent(b,pos)

        self.num_agents = N
        self.grid = MultiGrid(w, h, False)
        self.schedule = RandomActivation(self)

        rampas = [
            (2,21),
            (4,8),
            (5,26),
            (5,17),
            (5,5),
            (12,2),
            (10,20),
            (12,30),
            (13,17),
            (15,24),
            (23,30),
            (24,29),
            (23,8),
            (24,9),
            (24,17),
            (27,26),
            (28,25),
            (28,22),
            (29,5),
            (30,4),
            (13,11)
        ]

        streets = {}
        streets['up'] = []
        streets['down'] = []
        streets['left'] = []
        streets['right'] = []

        # Mapeo de direcciones
        # Arriba
        for x in range(31,33):
            for y in range(0,33):
                streets["up"].append((x,y))
        for x in range(25,27):
            for y in range(25,32):
                streets["up"].append((x,y))    
        for x in range(19,21):
            for y in range(17,32):
                streets["up"].append((x,y))
        for x in range(19,21):
            for y in range(2,12):
                streets["up"].append((x,y))

        # Abajo
        for x in range(16,18):
            for y in range(16,30):
                streets["down"].append((x,y))
        for x in range(16,18):
            for y in range(1,12):
                streets["down"].append((x,y))
        for x in range(16,18):
            for y in range(16,30):
                streets["down"].append((x,y))
        for x in range(8,10):
            for y in range(16,31):
                streets["down"].append((x,y))
        for x in range(25,27):
            for y in range(1,11):
                streets["down"].append((x,y))
        for x in range(0,2):
            for y in range(0,33):
                streets["down"].append((x,y))
        
        # Derecha ->
        for x in range(2,17):
            for y in range(12,14):
                streets["right"].append((x,y))
        for x in range(21,32):
            for y in range(12,14):
                streets["right"].append((x,y))
        for x in range(21,32):
            for y in range(23,25):
                streets["right"].append((x,y))
        for x in range(2,17):
            for y in range(6,8):
                streets["right"].append((x,y))
        for x in range(0,33):
            for y in range(0,2):
                streets["right"].append((x,y))
        
        # Izquierda <-
        for x in range(0,33):
            for y in range(31,33):
                streets["left"].append((x,y))
        for x in range(1,8):
            for y in range(24,26):
                streets["left"].append((x,y))
        for x in range(1,16):
            for y in range(15,17):
                streets["left"].append((x,y))
        for x in range(20,31):
            for y in range(15,17):
                streets["left"].append((x,y))
        for x in range(20,31):
            for y in range(6,8):
                streets["left"].append((x,y))

        # DIRECCIONES GLORIETA
        for y in range(12,16):
            streets["down"].append((16,y))
        for y in range(13,16):
            streets["up"].append((20,y))
        for x in range(16,21):
            streets["left"].append((x,16))
        for x in range(16,21):
            streets["right"].append((x,12))

        # Dictado de estacionamientos
        parks = {
            1 :(3,21),
            2 :(4,9),
            3 :(5,27),
            4 :(5,18),
            5 :(5,4),
            6 :(11,20),
            7 :(12,29),
            8 :(12,3),
            9 :(13,18),
            10:(13,10),
            11:(14,24),
            12:(23,29),
            13:(23,9),
            14:(24,18),
            15:(28,26),
            16:(28,21),
            17:(29,4)
        }

        # Diccionario de paradas
        busStop = {
            1: (2,29),
            2: (3,2),
            3: (22,2),
            4: (30,29)
        }

        # Crear y colocar agentes `car`
        car_pairs = [
            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),

            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
             (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
             (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
            (parks[1],parks[17]),
            (parks[2],parks[16]),
            (parks[3],parks[15]),
            (parks[14],parks[4]),
            (parks[5],parks[13]),
            (parks[12],parks[16]),
            (parks[7],parks[11]),
            (parks[10],parks[16]),
            (parks[9],parks[11]),
        ]
        print(len(car_pairs))

        # Posicionamiento de Grua
        grua_Start = [
            (1,1)
        ]

        gruas = []

        for x in grua_Start:
            grua = Grua(self.agentsCount,self,streets,busStop)
            gruas.append(grua)
            self.schedule.add(grua)
            self.grid.place_agent(grua, x)
            self.agentsCount += 1


        for start, end in car_pairs:
            c = Car(self.agentsCount, self, streets,start, end,parks, gruas)
            self.schedule.add(c)
            self.grid.place_agent(c, start)
            self.agentsCount += 1

        # Posicionamiento de Ambulancia
        ambulancia_Start = [
            (1,12)
        ]

        ambulancias = []

        for x in ambulancia_Start:
            ambulancia = Ambulancia(self.agentsCount,self,streets,busStop)
            ambulancias.append(ambulancia)
            self.schedule.add(ambulancia)
            self.grid.place_agent(ambulancia, x)
            self.agentsCount += 1

        # Posicionamiento de BUS

        bus_Start = [
            (1,31)
        ]

        for x in bus_Start:
            bus = Bus(self.agentsCount,self,streets,busStop,ambulancias)
            self.schedule.add(bus)
            self.grid.place_agent(bus, x)
            self.agentsCount += 1

        # agregar un cruce
        c = Cruce(1, self)
        self.schedule.add(c)
        self.grid.place_agent(c, (2, 6))
        self.grid.place_agent(c, (2, 7))
        self.grid.place_agent(c, (2, 24))
        self.grid.place_agent(c, (2, 25))
        self.grid.place_agent(c, (8, 17))
        self.grid.place_agent(c, (9, 17))
        self.grid.place_agent(c, (8, 30))
        self.grid.place_agent(c, (9, 30))
        self.grid.place_agent(c, (15, 6))
        self.grid.place_agent(c, (15, 7))
        self.grid.place_agent(c, (25, 5))
        self.grid.place_agent(c, (26, 5))
        self.grid.place_agent(c, (24, 6))
        self.grid.place_agent(c, (24, 7))
        self.grid.place_agent(c, (25, 8))
        self.grid.place_agent(c, (26, 8))
        self.grid.place_agent(c, (27, 6))
        self.grid.place_agent(c, (27, 7))
        self.grid.place_agent(c, (25, 30))
        self.grid.place_agent(c, (26, 30))
        self.grid.place_agent(c, (21, 24))
        self.grid.place_agent(c, (21, 23))
        self.grid.place_agent(c, (30, 24))
        self.grid.place_agent(c, (30, 23))

        # agregar un peaton
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.agentsCount+=1
        self.grid.place_agent(p, (2, 2))
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(15,4))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(2,30))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(15,17))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(21,30))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(25,17))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(21,11))
        self.agentsCount+=1
        p = Peaton(self.agentsCount, self, ambulancias)
        self.schedule.add(p)
        self.grid.place_agent(p,(27,8))
        self.agentsCount+=1

        # Posicionamiento semaforo
        semaforo_positions = [
                ((0,26), "rojo"), ((1,26), "rojo"), ((2, 25), "verde"), ((2,24), "verde"),
                ((27, 32), "verde"), ((27, 31), "verde"), ((30, 25), "rojo"), ((30, 26), "rojo"),
                ((30,24), "verde"), ((30,23), "verde"), ((31, 22), "rojo"), ((32, 22), "rojo"),
                ((25, 8), "rojo"), ((26, 8), "rojo"), ((27, 7), "verde"), ((27, 6), "verde"),
                ((15, 7), "verde"), ((15, 6), "verde"), ((16,8), "rojo"), ((17,8), "rojo")
            ]

        semaforo_ID = 200

        for pos, estado_inicial in semaforo_positions:
                semaforo = Semaforo(semaforo_ID, self, estado_inicial)
                self.schedule.add(semaforo)
                self.grid.place_agent(semaforo, pos)
                semaforo_ID += 1

        # Lista de áreas de Builds
        build_cells = []
        for x in range(3,7):
            for y in range(27,30):
                build_cells.append((x,y))
        for x in range(11,15):
            for y in range(18,30):
                build_cells.append((x,y))
        for x in range(3,7):
            for y in range(18,23):
                build_cells.append((x,y))
        for x in range(22,30):
            for y in range(18,22):
                build_cells.append((x,y))
        for x in range(22,24):
            for y in range(26,30):
                build_cells.append((x,y))
        for x in range(28,30):
            for y in range(26,30):
                build_cells.append((x,y))
        for x in range(22,24):
            for y in range(9,11):
                build_cells.append((x,y))
        for x in range(22,24):
            for y in range(3,5):
                build_cells.append((x,y))
        for x in range(28,30):
            for y in range(9,11):
                build_cells.append((x,y))
        for x in range(28,30):
            for y in range(3,5):
                build_cells.append((x,y))
        for x in range(3,15):
            for y in range(9,11):
                build_cells.append((x,y))
        for x in range(3,15):
            for y in range(3,5):
                build_cells.append((x,y))

        # Posicionamiento de Builds, Parks y Banquetas

        # GLORIETA Y AVENIDAS
        i = 0
        for x in range(2,16):
            build_cells.append((x,14))
            building(self,(x,14),build_cells,parks,rampas,busStop,i)
            i+=1
        for x in range(21,31):
            build_cells.append((x,14))
            building(self,(x,14),build_cells,parks,rampas,busStop,i)
            i+=1

        for y in range(17,31):
            build_cells.append((18,y))
            building(self,(18,y),build_cells,parks,rampas,busStop,i)
            i+=1
        
        for y in range(2,12):
            build_cells.append((18,y))
            building(self,(18,y),build_cells,parks,rampas,busStop,i)
            i+=1
        
        for x in range(17,20):
            for y in range(13,16):
                build_cells.append((x,y))
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1

        # Edificios
        for x in range(2,8):
            for y in range(26,31):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1  
        for x in range(2,16):
            for y in range(2,6):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(2,16):
            for y in range(8,12):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(2,8):
            for y in range(17,24):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(10,16):
            for y in range(17,31):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(21,31):
            for y in range(17,23):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(21,25):
            for y in range(25,31):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(27,31):
            for y in range(25,31):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1

        for x in range(21,25):
            for y in range(2,6):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(27,31):
            for y in range(2,6):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(21,25):
            for y in range(8,12):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1
        for x in range(27,31):
            for y in range(8,12):
                building(self,(x,y),build_cells,parks,rampas,busStop,i)
                i+=1

    def step(self):
        self.schedule.step()