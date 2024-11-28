using UnityEngine;

public class Cambio_Camaras : MonoBehaviour
{
    public GameObject[] Listacamaras;
    int ncamara = 7;
    void Start()
    {
     for(int i=0; i<ncamara; i++)
     {
         Listacamaras[i].gameObject.SetActive(false);
     }
     Listacamaras[0].gameObject.SetActive(true);
    }

    void ApagarCamaras() {
        for(int i=0; i<ncamara; i++){
            Listacamaras[i].gameObject.SetActive(false);
        }
    }

    void Update()
    {
        if(Input.GetKey(KeyCode.Alpha1))
        {
            ApagarCamaras();
            Listacamaras[0].gameObject.SetActive(true);
        }
         if(Input.GetKey(KeyCode.Alpha2))
        {
            ApagarCamaras();
            Listacamaras[1].gameObject.SetActive(true);
        }
         if(Input.GetKey(KeyCode.Alpha3))
        {
            ApagarCamaras();
            Listacamaras[2].gameObject.SetActive(true);
        }
         if(Input.GetKey(KeyCode.Alpha4))
        {
            ApagarCamaras();
            Listacamaras[3].gameObject.SetActive(true);
        }
         if(Input.GetKey(KeyCode.Alpha5))
        {
            ApagarCamaras();
            Listacamaras[4].gameObject.SetActive(true);
        }
         if(Input.GetKey(KeyCode.Alpha6))
        {
            ApagarCamaras();
            Listacamaras[5].gameObject.SetActive(true);  
        }
         if(Input.GetKey(KeyCode.Alpha7))
        {
           ApagarCamaras();
           Listacamaras[6].gameObject.SetActive(true);
        }
    }
}
