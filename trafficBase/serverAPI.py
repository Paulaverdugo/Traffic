# old
from flask import Flask, request, jsonify
from model import CityModel
from agent import Car, Traffic_Light, Destination, Obstacle, Road
import requests
import json

# Configuración inicial del modelo y otras definiciones...
app = Flask("Traffic Simulation")


# Configuración inicial del modelo:
number_agents = 10
width = 28
height = 28
trafficModel = None
currentStep = 0

@app.route('/post_car_count', methods=['GET'])
def post_car_count():
    global trafficModel

    # Contar el número de coches en la simulación
    num_cars = len([a for a in trafficModel.schedule.agents if isinstance(a, Car)])

    # Datos a enviar
    data = {
        "year": 2023,
        "classroom": 302,
        "name": "Equipo2",
        "num_cars": num_cars
    }

    # URL del endpoint externo
    url = "http://52.1.3.19:8585/api/validate_attempt"

    # Realizar el POST al endpoint externo
    response = requests.post(url, json=data)

    # Crear una respuesta para esta solicitud
    return jsonify({"message": "Data posted", "response": response.json(), "status_code": response.status_code})


@app.route('/validate_attempt', methods=['POST'])
def validate_attempt():
    global trafficModel

    data = request.get_json()
    data["num_cars"] = len([a for a in trafficModel.schedule.agents if isinstance(a, Car)])

    # External API URL and endpoint
    url = "http://localhost:5000/api/"
    endpoint = "validate_attempt"

    headers = {
        "Content-Type": "application/json"
    }

    # Sending the data to the external API
    response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)

    # Create a response for the POST request
    if response.status_code == 200:
        return jsonify({"message": "Request successful", "response": response.json()})
    else:
        return jsonify({"message": "Request failed", "status_code": response.status_code})


@app.route('/init', methods=['GET', 'POST'])
def initModel():
    global currentStep, trafficModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = 0
        try:
            number_agents = int(request.form.get('NAgents'))
        except:
            number_agents = 1
            
        currentStep = 0
        trafficModel = CityModel(number_agents)
        return jsonify({"message": "Model initialized with custom parameters."})
    elif request.method == 'GET':
        trafficModel = CityModel(number_agents)
        return jsonify({"message": "Model initialized with default parameters."})

@app.route('/getTrafficLights', methods=['GET'])
def getTrafficLights():
    global trafficModel

    if request.method == 'GET':
        trafficLightStates = [{"id": str(tl.unique_id), "state": tl.state}
                              for tl in trafficModel.traffic_lights]
        return jsonify({'trafficLights': trafficLightStates})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global trafficModel

    if request.method == 'GET':
        agentPositions = [{"id": str(a.unique_id), "x": a.pos[0], "y": 0, "z": a.pos[1]}
                          for a in trafficModel.schedule.agents
                          if isinstance(a, Car)]
        return jsonify({'agents': agentPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, trafficModel

    if request.method == 'GET':
        trafficModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.', 'currentStep': currentStep})

if __name__ == '__main__':
    app.run(host="localhost", port=8583, debug=True)

    