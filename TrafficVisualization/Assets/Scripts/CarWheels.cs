using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarWheels : MonoBehaviour
{
    [SerializeField] private Vector3 startPosition;
    [SerializeField] private Vector3 stopPosition;
    [SerializeField] private float angle;
    [SerializeField] private GameObject wheelPrefab; 
    [SerializeField] private Vector3 wheelScale = new Vector3(1f, 1f, 1f); // Escala para las ruedas

    private float t;
    private float elapsedTime = 0.0f;
    private float moveTime = 5.0f; // = tiempo que tenga agent controller? que lo pase agent controller
    private Vector3 startPos;
    private Vector3 finalPos;

    private Vector3[] baseVertices;
    private Vector3[] newVertices;

    private Mesh mesh;


    private Vector3 frontAxis = new Vector3(1.1f, 0.12f, -8.65f);
    private Vector3 backAxis = new Vector3(1.1f, 0.12f, -6f);

    private GameObject[] wheels = new GameObject[4];

    // Start is called before the first frame update
    void Start()
    {
        // // Crear instancias de las ruedas en las posiciones correctas
        // wheels[0] = Instantiate(wheelPrefab, frontAxis, Quaternion.identity, transform);
        // wheels[1] = Instantiate(wheelPrefab, Vector3.Scale(frontAxis, new Vector3(-1, 1, 1)), Quaternion.identity, transform);
        // wheels[2] = Instantiate(wheelPrefab, backAxis, Quaternion.identity, transform);
        // wheels[3] = Instantiate(wheelPrefab, Vector3.Scale(backAxis, new Vector3(-1, 1, 1)), Quaternion.identity, transform);

        // foreach (GameObject wheel in wheels)
        // {
        //     wheel.transform.localScale = wheelScale;
        // }

        // // Crear el mesh
        MeshFilter meshFilter = GetComponent<MeshFilter>();
        mesh = meshFilter.mesh;
        baseVertices = mesh.vertices;
        newVertices = new Vector3[baseVertices.Length];
    }

    // Update is called once per frame
    void Update()
    {
        MoveCar();
        // RotateWheels();
    }

    private void MoveCar()
        // Mover el coche hacia adelante
        //  ir imprimiento las pos
    {
        t = elapsedTime / moveTime;
        // t = t * t * (3.0f - 2.0f * t);

        Vector3 position = startPos + (finalPos - startPos) * t; 
        Debug.Log(position);


        // Using the Unity transforms
        Matrix4x4 move = HW_Transforms.TranslationMat(position.x,
                                                      position.y,
                                                      position.z);

        Matrix4x4 composite = move;

        // Multiply each vertex in the mesh by the composite matrix
        for (int i=0; i<newVertices.Length; i++) {
            Vector4 temp = new Vector4(baseVertices[i].x,
                                       baseVertices[i].y,
                                       baseVertices[i].z,
                                       1);
            newVertices[i] = composite * temp;
        }

        // Replace the vertices in the mesh
        mesh.vertices = newVertices;
        // Make sure the normals are adapted to the new vertex positions
        mesh.RecalculateNormals();
        // Let the renderer know the vertex positions changed
        mesh.RecalculateBounds();


        elapsedTime += Time.deltaTime;

        if (elapsedTime >= moveTime) {

            elapsedTime = moveTime;
        }

    }

    public void SetNewPosition(Vector3 newPosition)
    {   
        // es donde comienzo de nuevo por que ya llegaste
        startPosition = stopPosition;
        stopPosition = newPosition;
        elapsedTime = 0.0f;
    }

    private void RotateWheels()
    {
        // Rotar las ruedas
        foreach (GameObject wheel in wheels)
        {
            wheel.transform.Rotate(Vector3.right, angle * Time.deltaTime);
        }
    }

    public void SetTimer(float time)
    {
        moveTime = time;
    }


}
