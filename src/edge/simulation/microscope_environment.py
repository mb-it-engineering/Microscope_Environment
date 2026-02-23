import numpy as np
import cv2
from edge.simulation.metrics import compute_metrics

class MicroscopeEnv:
    def __init__(self, image_size=256):
        self.image_size = image_size
        self.reset()

    def reset(self):
        self.exposure = 50.0
        self.laser_power = 1.0
        self.gain = 1.0
        self.z_offset = 3.0
        self.bleaching = 1.0

        self._generate_ground_truth()

    def _generate_ground_truth(self):
        img = np.zeros((self.image_size, self.image_size), dtype=np.float32)

        for _ in range(20):
            x, y = np.random.randint(0, self.image_size, 2)
            sigma = np.random.uniform(3, 8)
            xv, yv = np.meshgrid(
                np.arange(self.image_size),
                np.arange(self.image_size)
            )
            gauss = np.exp(-((xv - x) ** 2 + (yv - y) ** 2) / (2 * sigma ** 2))
            img += gauss

        img /= img.max()
        self.ground_truth = img

    def set_parameter(self, name, value):
        setattr(self, name, float(value))

    def get_parameters(self):
        return {
            "exposure": self.exposure,
            "laser_power": self.laser_power,
            "gain": self.gain,
            "z_offset": self.z_offset,
            "bleaching": self.bleaching
        }

    def capture(self):
        # --- Signal strength ---
        # exposure: longer exposure = more collected photons (linear)
        # laser_power: higher power = more excited fluorophores (linear)
        # bleaching: permanently reduces signal strength over time
        signal = self.ground_truth * self.laser_power * (self.exposure / 50.0) * self.bleaching

        # --- Defocus (z_offset) ---
        # z_offset == 0 → sharp; the further away, the stronger the blur
        # A minimum blur of 0.5 always remains, simulating the optical diffraction limit
        defocus_sigma = max(0.5, abs(self.z_offset))
        signal = cv2.GaussianBlur(signal.astype(np.float32), (0, 0), defocus_sigma)

        # At strong defocus, peak intensity drops (energy is conserved but
        # spread over a larger area → local brightness decreases)
        if abs(self.z_offset) > 0.5:
            spread_factor = 1.0 / (1.0 + 0.1 * self.z_offset ** 2)
            signal *= spread_factor

        # --- Photon noise (Poisson) ---
        # Scaling by exposure + laser_power: more photons → relative noise decreases
        photon_scale = max(1.0, self.exposure * self.laser_power)
        dark_current = 0.01  # thermal noise / dark current
        counts = np.clip(signal * photon_scale + dark_current, 0, None)
        noisy = np.random.poisson(counts).astype(np.float32) / photon_scale

        # --- Gain ---
        # Gain amplifies signal AND read noise equally.
        # High gain → brighter image, but also more visible noise.
        read_noise_sigma = 0.02 * self.gain  # read noise scales with gain
        noisy = self.gain * noisy
        noisy += np.random.normal(0, read_noise_sigma, noisy.shape)

        # Gain > 1 can cause overexposure → clipping simulates sensor saturation
        noisy = np.clip(noisy, 0, self.gain)  # saturation limit = gain
        noisy /= max(self.gain, 1.0)          # normalize to [0, 1]

        # --- Bleaching ---
        # Fluorophores are permanently degraded with each capture
        # Higher laser power accelerates the bleaching process
        bleach_rate = 0.995 - 0.003 * (self.laser_power - 1.0)
        self.bleaching *= max(0.9, bleach_rate)  # min 0.9 per frame

        metrics = compute_metrics(noisy)
        return noisy, metrics