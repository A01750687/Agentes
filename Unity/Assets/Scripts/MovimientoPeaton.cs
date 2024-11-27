using UnityEngine;

public class MovimientoPeaton : MonoBehaviour
{
    public float NuevaposX;
    public float NuevaposY;

    // Update is called once per frame
    void Update()
    {
        Vector3 targetPosition = new Vector3(NuevaposX, transform.position.y, NuevaposY); // Mantiene la misma altura en Y
        Vector3 targetDir = targetPosition - transform.position;
        targetDir.y = 0; // Ignoramos la componente Y para rotar solo en el eje Y

        if (targetDir != Vector3.zero)
        {
            // Calculamos la rotación hacia la nueva dirección solo en el eje Y
            Quaternion targetRotation = Quaternion.LookRotation(targetDir, Vector3.up);

            // Aseguramos que la rotación en el eje X sea siempre 90 grados
            targetRotation = Quaternion.Euler(-90f, targetRotation.eulerAngles.y, 0f);

            // Interpolamos la rotación para que sea suave
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                targetRotation,
                Time.deltaTime * 45f // Ajusta la velocidad de rotación según sea necesario
            );

            // Movemos el objeto hacia la nueva posición
            transform.position = Vector3.MoveTowards(transform.position, targetPosition, 5f * Time.deltaTime);
        }
    }
}
