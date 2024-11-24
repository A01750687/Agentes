using UnityEngine;
using System.Collections;

public class Inicio : MonoBehaviour
{
    private FlaskConnection flaskConnection;

    // Se ejecuta al iniciar
    void Start()
    {
        // Obtener el componente FlaskConnection desde el mismo GameObject o de otro objeto
        flaskConnection = GetComponent<FlaskConnection>();

        if (flaskConnection != null)
        {
            // Llamar a GetCoordinatesFromFlask una vez antes de comenzar el ciclo
            StartCoroutine(CallGetCoordinatesRepeatedly());
        }
        else
        {
            Debug.LogError("FlaskConnection component not found!");
        }
    }

    IEnumerator CallGetCoordinatesRepeatedly()
    {
        while (true) // Esto mantiene la solicitud en un bucle
        {
            yield return new WaitForSeconds(1f);
            StartCoroutine(flaskConnection.GetCoordinatesFromFlask());
        }
    }
}
