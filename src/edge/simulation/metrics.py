import numpy as np
import cv2
import matplotlib.pyplot as plt

def plot_metrics(epochs):
    times = sorted(epochs.keys())
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes_twin_0 = axes[0][0].twinx()
    axes[0][0].plot(times, [epochs[i]["saturation_pct"] for i in times], label='Saturation')
    axes[0][0].set_xlabel("Epoch")
    axes[0][0].set_ylabel("Saturation (%)")
    axes[0][0].legend()
    axes_twin_0.plot(times, [epochs[i].get("exposure", 0) for i in times], label='Exposure', color='green', linestyle='--')
    axes_twin_0.set_ylabel("Exposure", color='green')
    
    axes_twin_1 = axes[0][1].twinx()
    axes[0][1].plot(times, [epochs[i]["focus_score"] for i in times], label='Focus Score', color='orange')
    axes[0][1].set_xlabel("Epoch")
    axes[0][1].set_ylabel("Focus Score")
    axes[0][1].legend()
    axes_twin_1.plot(times, [epochs[i].get("z_offset", 0) for i in times], label='z_offset', color='blue', linestyle='--')
    axes_twin_1.set_ylabel("z_offset", color='blue')    

    axes_twin_3 = axes[1][0].twinx()
    axes[1][0].plot(times, [epochs[i]["snr"] for i in times], label='SNR', color='purple')
    axes[1][0].set_xlabel("Epoch")
    axes[1][0].set_ylabel("SNR (dB)")
    axes[1][0].legend()
    axes_twin_3.set_ylabel("Exposure", color='green')
    axes_twin_3.plot(times, [epochs[i].get("exposure", 0) for i in times], label='Exposure', color='green', linestyle='--')

    axes_twin_4 = axes[1][1].twinx()
    axes[1][1].plot(times, [epochs[i]["mean_intensity"] for i in times], label='Mean Intensity', color='magenta')
    axes[1][1].set_xlabel("Epoch")
    axes[1][1].set_ylabel("Mean Intensity")
    axes[1][1].legend()
    axes_twin_4.set_ylabel("Laser Power", color='red')
    axes_twin_4.plot(times, [epochs[i].get("laser_power", 0) for i in times], label='Laser Power', color='red', linestyle='--')
    
    plt.tight_layout()
    plt.show()

def compute_metrics(image: np.ndarray) -> dict:
    image = image.astype(np.float32)

    # Mean intensity across the whole image
    mean_intensity = float(np.mean(image))

    # Saturation: fraction of pixels close to sensor maximum
    saturation = float(np.mean(image >= 0.98) * 100)

    # Separate background and signal by a fixed threshold
    # Background = dim but non-zero pixels (exclude pure black)
    # Signal = bright pixels (top 10%)
    p90 = np.percentile(image, 90)
    signal = image[image >= p90]

    # Background: pixels above noise floor but below signal
    noise_floor = 1e-4
    background = image[(image > noise_floor) & (image < p90)]

    bg_std = float(np.std(background)) if len(background) > 10 else None

    if bg_std is not None and bg_std > 1e-6:
        snr = float(np.mean(signal) / bg_std)
    else:
        # Fallback: use read noise estimate when background is too clean
        snr = float(np.mean(signal) / 0.02)
    
    # Focus score: Laplacian variance, but pre-smoothed to suppress noise influence
    smoothed = cv2.GaussianBlur(image, (3, 3), 0)
    lap = cv2.Laplacian(smoothed, cv2.CV_32F)
    focus_score = float(lap.var())

    return {
        "mean_intensity": mean_intensity,
        "saturation_pct": saturation,
        "snr": snr,
        "focus_score": focus_score,
    }
