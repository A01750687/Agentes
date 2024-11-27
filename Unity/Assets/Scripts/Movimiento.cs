using UnityEngine;

public class Movimiento : MonoBehaviour
{    
    public float NuevaposX;

    public float NuevaposY;

    // Update is called once per frame
    void Update()
    {
        Vector3 targetPosition = new Vector3(NuevaposX, 0.0f, NuevaposY);
        // Calcular la dirección hacia el objetivo
        Vector3 targetDir = targetPosition - transform.position;
        // Mantener solo el movimiento horizontal (en el plano XZ)
        targetDir.y = 0;
        if (targetDir != Vector3.zero)
        {
            Quaternion targetRotation = Quaternion.LookRotation(targetDir, Vector3.up);
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                targetRotation,
                Time.deltaTime * 45f // Ajusta rotationSpeed
            );
        transform.position = Vector3.MoveTowards(transform.position, targetPosition,5f * Time.deltaTime);
        }
    }
}
