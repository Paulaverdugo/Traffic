using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarWheels : MonoBehaviour
{
    [SerializeField] private Vector3 displacement;
    [SerializeField] private float angle;
    [SerializeField] private GameObject wheelPrefab; 
    [SerializeField] private Vector3 wheelScale = new Vector3(1f, 1f, 1f); // Escala para las ruedas

    private Vector3 frontAxis = new Vector3(1.1f, 0.12f, -8.65f);
    private Vector3 backAxis = new Vector3(1.1f, 0.12f, -6f);

    private GameObject[] wheels = new GameObject[4];

    // Start is called before the first frame update
    void Start()
    {
        // Crear instancias de las ruedas en las posiciones correctas
        wheels[0] = Instantiate(wheelPrefab, frontAxis, Quaternion.identity, transform);
        wheels[1] = Instantiate(wheelPrefab, Vector3.Scale(frontAxis, new Vector3(-1, 1, 1)), Quaternion.identity, transform);
        wheels[2] = Instantiate(wheelPrefab, backAxis, Quaternion.identity, transform);
        wheels[3] = Instantiate(wheelPrefab, Vector3.Scale(backAxis, new Vector3(-1, 1, 1)), Quaternion.identity, transform);

        foreach (GameObject wheel in wheels)
        {
            wheel.transform.localScale = wheelScale;
        }
    }

    // Update is called once per frame
    void Update()
    {
        MoveCar();
        RotateWheels();
    }

    private void MoveCar()
    {
        // Mover el coche hacia adelante
        transform.Translate(displacement * Time.deltaTime);
    }

    private void RotateWheels()
    {
        // Rotar las ruedas
        foreach (GameObject wheel in wheels)
        {
            wheel.transform.Rotate(Vector3.right, angle * Time.deltaTime);
        }
    }
}
