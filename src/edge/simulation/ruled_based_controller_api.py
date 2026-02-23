
import requests
from edge.simulation.metrics import plot_metrics

if __name__ == "__main__":

    response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "z_offset", "value": 3.0})
    epochs = {} 

    for n in range(20):
        _, metrics = requests.post("http://localhost:8000/execute/capture", json={}).json()["result"].values()
        parameters = requests.post("http://localhost:8000/execute/get_parameters", json={}).json()["result"]
        epochs[n] = {**parameters, **metrics}
        if n > 0 and metrics["focus_score"] <= epochs[n-1]["focus_score"]:
            response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "z_offset", "value": parameters["z_offset"] - 0.5})

        if metrics["saturation_pct"] > 5:
            response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "exposure", "value": parameters["exposure"] * 0.8})

        elif metrics["snr"] < 15:
            response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "exposure", "value": parameters["exposure"] * 1.2})

        elif metrics["mean_intensity"] < 0.1:
            response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "laser_power", "value": parameters["laser_power"] * 1.2})
        
        print(f"Loop {n}: {metrics} \n Parameters: {parameters}")


    plot_metrics(epochs)
