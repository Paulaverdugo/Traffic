# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git

from flask import Flask, request, jsonify
from randomAgents.model import RandomModel
from randomAgents.agent import RandomAgent, ObstacleAgent
from flask import Flask, request, jsonify
from traffic_model import TrafficModel  # Asegúrate de que este importe corresponda a tu modelo
from traffic_agent import Car, TrafficLight  # Importa las clases de tus agentes

# Configuración inicial del modelo:
number_agents = 10
width = 28
height = 28
trafficModel = None
currentStep = 0

app = Flask("Traffic Simulation")

@app.route('/init', methods=['GET', 'POST'])
def initModel():
    global currentStep, trafficModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0
        trafficModel = TrafficModel(number_agents, width, height)
        return jsonify({"message": "Model initialized with custom parameters."})
    elif request.method == 'GET':
        trafficModel = TrafficModel(number_agents, width, height)
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
        agentPositions = [{"id": str(a.unique_id), "x": a.pos[0], "y": a.pos[1]}
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
    app.run(host="localhost", port=8585, debug=True)
