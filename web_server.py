import asyncio
import logging
from flask import Flask , request , jsonify
from flask_socketio import SocketIO
from drone_controller import DroneController

# flask app initialisation
app = Flask(__name__)

socketio = SocketIO(app , async_mode='threading')

drone = DroneController("udp:127.0.0.1:14550")

@app.route("/takeoff" , methods = ['POST'])
def takeoff():
    
    try:
        drone.takeoff()
        return jsonify({"message": "takeoff initiated"}) , 200
    
    except Exception as e:
        logging.error(f"Error in takeoff{e}")
        return jsonify({"error" : str(e)}) , 500

@app.route("/land" , methods = ['POST'])
def land():
    try:
        drone.land()
        return jsonify({"message" : "landing initiated"}) , 200
    except Exception as e:
        logging.error(f"unable to land reason {e}")
        return jsonify({"error" : str(e)}) , 500
    
@app.route("/return_home" , methods = ['POST'])
def return_home():
    try:
         drone.return_home()
         return jsonify({"message" : "initiated RTL"}) , 200
    except Exception as e:
        logging.error(f"error in RTL{e}")
        return jsonify({"error":str(e)}) , 500
    
@app.route("/move", methods=["POST"])
def move():
    try:
        data = request.get_json()
        vx, vy, vz = data.get("vx", 0), data.get("vy", 0), data.get("vz", 0)
        drone.move(vx, vy, vz)
        return jsonify({"message": "Drone moving"}), 200
    except Exception as e:
        logging.error(f"Error in move: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/stop", methods=["POST"])
def stop():
    try:
        drone.stop()
        return jsonify({"message": "Drone stopped"}), 200
    except Exception as e:
        logging.error(f"Error in stop: {e}")
        return jsonify({"error": str(e)}), 500

    
@socketio.on("telemetry")
def send_telemetry():
    while True:
        telemetry = drone.get_telemetry()
        if telemetry:
            socketio.emit("telemetry", telemetry)
        socketio.sleep(1)  # Send updates every second

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
    
