using UnityEngine;
using UnityEngine.Networking;  // Para solicitudes HTTP
using System.Collections;
using System.Collections.Generic;
using System;  // Necesario para usar Dictionary

public class FlaskConnection : MonoBehaviour
{
    public List<GameObject> prefabCars;
    public GameObject prefabBus;

    public GameObject prefabAmbulance;

    public GameObject prefabGrua;

    public List<GameObject> prefabPeatones;

    public List<GameObject> semaforos;

    private Boolean dictadoCreado = false;

    private Dictionary<int,GameObject> semaforosDict = new Dictionary<int, GameObject>();

    private string flaskUrl = "http://127.0.0.1:5000"; // Dirección del servidor Flask

    // Diccionario para mantener las referencias a los coches creados
    private Dictionary<int, GameObject> cars = new Dictionary<int, GameObject>();

    // Diccionario para mantener las referencias a los buses creados
    private Dictionary<int, GameObject> buses = new Dictionary<int, GameObject>();

    // Diccionario para mantener las referencias a los peatones creados
    private Dictionary<int, GameObject> peatones = new Dictionary<int, GameObject>();

    // Diccionario para mantener las referencias a los peatones creados
    private Dictionary<int, GameObject> ambulancias = new Dictionary<int, GameObject>();

    // Diccionario para mantener las referencias a los peatones creados
    private Dictionary<int, GameObject> gruas = new Dictionary<int, GameObject>();

    // Método para obtener coordenadas desde Flask y actualizar la posición de los coches
    public IEnumerator GetCoordinatesFromFlask()
    {

        if(!dictadoCreado){
            var semaforos_id = 200;

            foreach(var semaforo in semaforos){
                semaforosDict.Add(semaforos_id, semaforo);
                semaforos_id += 2;
            }
            dictadoCreado = true;
        }

        // Llama a las posiciones de coches
        UnityWebRequest request = UnityWebRequest.Get($"{flaskUrl}/get_car_positions");
        yield return request.SendWebRequest();
        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request.downloadHandler.text;

            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");

            int listLength = prefabCars.Count;

            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.3433f, coords.y);
                int randomVal = UnityEngine.Random.Range(0,listLength);
                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                if (cars.ContainsKey(coords.id))
                {
                    GameObject car = cars[coords.id];
                    Movimiento script = car.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject car = Instantiate(prefabCars[randomVal], targetPosition, Quaternion.identity);
                    Movimiento script = car.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                    cars.Add(coords.id, car);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request.error}");
        }

        // Llama a las posiciones de buses
        UnityWebRequest request2 = UnityWebRequest.Get($"{flaskUrl}/get_bus_positions");
        yield return request2.SendWebRequest();
        if (request2.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request2.downloadHandler.text;

            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.0f, coords.y);

                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                if (buses.ContainsKey(coords.id))
                {
                    GameObject bus = buses[coords.id];
                    Movimiento script = bus.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject bus = Instantiate(prefabBus, targetPosition, Quaternion.identity);
                    Movimiento script = bus.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                    buses.Add(coords.id, bus);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request2.error}");
        }

        // Llama a las posiciones de peatones
        UnityWebRequest request3 = UnityWebRequest.Get($"{flaskUrl}/get_peatones_positions");
        yield return request3.SendWebRequest();
        if (request3.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request3.downloadHandler.text;


            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            
            int listLength = prefabPeatones.Count;
            
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.3433f, coords.y);

                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                int randomVal = UnityEngine.Random.Range(0,listLength);
                if (peatones.ContainsKey(coords.id))
                {

                    GameObject peaton = peatones[coords.id];
                    MovimientoPeaton script = peaton.GetComponent<MovimientoPeaton>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;

                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject peaton = Instantiate(prefabPeatones[randomVal], targetPosition, Quaternion.identity);
                    MovimientoPeaton script = peaton.GetComponent<MovimientoPeaton>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                    peaton.transform.Rotate(-90,0,-185.11f);
                    peatones.Add(coords.id, peaton);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request3.error}");
        }

        // Llama a las posiciones de ambulancia
        UnityWebRequest request4 = UnityWebRequest.Get($"{flaskUrl}/get_ambulancia_positions");
        yield return request4.SendWebRequest();
        if (request4.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request4.downloadHandler.text;


            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            
            
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.0f, coords.y);

                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                if (ambulancias.ContainsKey(coords.id))
                {
                    GameObject ambulancia = ambulancias[coords.id];
                    Movimiento script = ambulancia.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject ambulancia = Instantiate(prefabAmbulance, targetPosition, Quaternion.identity);
                    Movimiento script = ambulancia.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                    ambulancias.Add(coords.id, ambulancia);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request4.error}");
        }

        // Llama a los estados del semaforo
        UnityWebRequest request5 = UnityWebRequest.Get($"{flaskUrl}/get_semaforos_state");
        yield return request5.SendWebRequest();
        if (request5.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request5.downloadHandler.text;


            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                GameObject semaforo = semaforosDict[coords.id];

                // Buscamos si el semáforo ya tiene un hijo llamado "Light"
                Transform existingLight = semaforo.transform.Find("Light");

                // Si no existe, creamos uno nuevo
                GameObject lightObject;
                if (existingLight == null)
                {
                    lightObject = new GameObject("Light");
                    lightObject.transform.parent = semaforo.transform; // Hacemos que la luz sea hijo del semáforo
                }
                else
                {
                    lightObject = existingLight.gameObject; // Usamos el objeto de luz existente
                }

                // Obtenemos o agregamos el componente de luz
                Light light = lightObject.GetComponent<Light>();
                if (light == null)
                {
                    light = lightObject.AddComponent<Light>(); // Si no tiene componente de luz, lo agregamos
                }

                // Configuramos la luz
                light.type = LightType.Point;  // Tipo de luz
                if (!coords.state) // Estado = falso, luz roja
                {
                    light.color = Color.red;
                    light.intensity = 1f;
                    light.range = 10f;
                }
                else // Estado = verdadero, luz verde
                {
                    light.color = Color.green;
                    light.intensity = 1f;
                    light.range = 10f;
                }

                // Colocamos la luz en la misma posición que el GameObject (semaforo)
                lightObject.transform.localPosition = Vector3.zero;  // Se coloca en la posición local del semáforo
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request5.error}");
        }

        // Llama a las posiciones de ambulancia
        UnityWebRequest request6 = UnityWebRequest.Get($"{flaskUrl}/get_grua_positions");
        yield return request6.SendWebRequest();
        if (request6.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request6.downloadHandler.text;


            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            
            
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.0f, coords.y);

                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                if (gruas.ContainsKey(coords.id))
                {
                    GameObject grua = gruas[coords.id];
                    Movimiento script = grua.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject grua = Instantiate(prefabGrua, targetPosition, Quaternion.identity);
                    Movimiento script = grua.GetComponent<Movimiento>();
                    script.NuevaposX = coords.x;
                    script.NuevaposY = coords.y;
                    gruas.Add(coords.id, grua);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request6.error}");
        }

    }

    
}

// Clase para manejar las coordenadas como JSON
[System.Serializable]
public class Coordinates
{
    public int id;
    public float x;
    public float y;
    public bool state;
}


// Clase para manejar una lista de coordenadas
[System.Serializable]
public class CoordinatesList
{
    public Coordinates[] coordinates;
}
