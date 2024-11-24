using UnityEngine;
using UnityEngine.Networking;  // Para solicitudes HTTP
using System.Collections;
using System.Collections.Generic;  // Necesario para usar Dictionary

public class FlaskConnection : MonoBehaviour
{
    public GameObject prefabCar;
    public GameObject prefabBus;

    private float movementSpeed = 30f;

    private string flaskUrl = "http://127.0.0.1:5000"; // Dirección del servidor Flask

    // Diccionario para mantener las referencias a los coches creados
    private Dictionary<int, GameObject> cars = new Dictionary<int, GameObject>();

    // Diccionario para mantener las referencias a los buses creados
    private Dictionary<int, GameObject> buses = new Dictionary<int, GameObject>();

    // Método para obtener coordenadas desde Flask y actualizar la posición de los coches
    public IEnumerator GetCoordinatesFromFlask()
    {
        UnityWebRequest request = UnityWebRequest.Get($"{flaskUrl}/get_car_positions");
        yield return request.SendWebRequest();
        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request.downloadHandler.text;

            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                Vector3 targetPosition = new Vector3(coords.x, 0.0f, coords.y);

                // Si ya existe un coche con ese ID, actualizamos su posición de forma fluida
                if (cars.ContainsKey(coords.id))
                {
                    GameObject car = cars[coords.id];
                    car.transform.position = targetPosition;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject car = Instantiate(prefabCar, targetPosition, Quaternion.identity);
                    cars.Add(coords.id, car);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request.error}");
        }

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
                    bus.transform.position = targetPosition;
                }
                else
                {
                    // Si no existe, creamos un nuevo coche
                    GameObject bus = Instantiate(prefabBus, targetPosition, Quaternion.identity);
                    buses.Add(coords.id, bus);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request2.error}");
        }
    }

    public IEnumerator getCars()
    {
        UnityWebRequest request = UnityWebRequest.Get($"{flaskUrl}/get_Cars");
        yield return request.SendWebRequest();
        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request.downloadHandler.text;

            // Si el JSON es una lista, usamos CoordinatesList
            CoordinatesList coordsList = JsonUtility.FromJson<CoordinatesList>("{\"coordinates\":" + jsonResult + "}");
            // Iteramos sobre la lista de coordenadas
            foreach (var coords in coordsList.coordinates)
            {
                // Verifica si el coche ya está creado para evitar duplicados
                if (!cars.ContainsKey(coords.id))
                {
                    Instantiate(prefabCar, new Vector3(coords.x, 0, coords.y), Quaternion.identity);
                }
            }
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request.error}");
        }
    }

    // Método para enviar coordenadas a Flask
    public IEnumerator SendCoordinatesToFlask(Vector3 coordinates)
    {
        Coordinates coords = new Coordinates
        {
            x = coordinates.x,
            y = coordinates.y,
        };

        string json = JsonUtility.ToJson(coords);
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);

        UnityWebRequest request = UnityWebRequest.Put($"{flaskUrl}/send_coordinates", jsonToSend);
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Coordinates sent successfully!");
        }
        else
        {
            Debug.LogError($"Error sending coordinates: {request.error}");
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
}


// Clase para manejar una lista de coordenadas
[System.Serializable]
public class CoordinatesList
{
    public Coordinates[] coordinates;
}
