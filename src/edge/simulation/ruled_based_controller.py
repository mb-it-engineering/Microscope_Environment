from edge.simulation.microscope_environment import MicroscopeEnv
import matplotlib.pyplot as plt
from edge.simulation.metrics import plot_metrics
import numpy as np

if __name__ == "__main__":
    env = MicroscopeEnv()
    radom_seed = 42
    np.random.seed(radom_seed)
    np.random.randint(0, 5) 
    env.set_parameter("z_offset", 3.0)
    epochs = {} 

    for n in range(20):
        _, metrics = env.capture()
        parameters = env.get_parameters()
        epochs[n] = {**parameters, **metrics}
        if n > 0 and metrics["focus_score"] <= epochs[n-1]["focus_score"]:
            env.set_parameter("z_offset", env.z_offset - 0.5)

        if metrics["saturation_pct"] > 5:
            env.set_parameter("exposure", env.exposure * 0.8)

        elif metrics["snr"] < 15:
            env.set_parameter("exposure", env.exposure * 1.2)

        elif metrics["mean_intensity"] < 0.1:
            env.set_parameter("laser_power", env.laser_power * 1.2)
        
        print(f"Loop {n}: {metrics} \n Parameters: {parameters}")


    plot_metrics(epochs)
