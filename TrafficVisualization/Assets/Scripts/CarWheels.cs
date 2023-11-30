using UnityEngine;

public class CarWheels : MonoBehaviour
{
    private Mesh mesh;
    private Vector3[] vertices;
    private Vector3[] baseVertices;
    private bool started = false;
    public float angle;

    //New
    private Vector3 destination;
    private bool hasArrived = false;
    private float arrivalThreshold = 0.5f;


    public void SetDestination(Vector3 newDestination)
    {
        destination = newDestination;
        hasArrived = false;
    }
    
    // Start is called before the first frame update
    public void Start(){
        if (!started) {
            mesh = GetComponentInChildren<MeshFilter>().mesh;
            vertices = mesh.vertices;
            baseVertices = new Vector3[vertices.Length];
            for (int i = 0; i < vertices.Length; i++){
                baseVertices[i] = vertices[i];
            }
        }
        this.started = true;
    }

    public void MoveCar(Vector3 position, Vector3 direction) {
        Matrix4x4 move = HW_Transforms.TranslationMat(
            position.x,
            position.y,
            position.z
        );

        if (direction.magnitude != 0) {
            this.angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;
        }

        Matrix4x4 rotate = HW_Transforms.RotateMat(
            this.angle,
            AXIS.Y
        );
        
        Matrix4x4 transform = move * rotate;

        for (int i = 0; i < vertices.Length; i++){
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            vertices[i] = transform * temp;
        }

        mesh.vertices = vertices;
        mesh.RecalculateNormals();
    }


    // public void SetNewPosition(Vector3 newPosition)
    // {
    //     if (this == null || gameObject == null)
    //     {
    //         // The object has been destroyed, so don't try to set a new position
    //         return;
    //     }

    //     startPos = finalPos;
    //     Debug.Log("Start pos: " + startPos);
    //     finalPos = newPosition;
    //     Debug.Log("Final pos: " + finalPos);
    //     //Ambos deben ser iguales
    //     elapsedTime = 0.0f;
    //     shouldMove = true;
    // }





    // public void SetTimer(float time)
    // {
    //     moveTime = time;
    // }
}