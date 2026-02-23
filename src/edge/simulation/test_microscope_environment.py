from edge.simulation.microscope_environment import MicroscopeEnv

env = MicroscopeEnv()

def test_capture():
    for i in range(5):
        img, metrics = env.capture()
        assert img.size > 0
        assert "focus_score" in metrics
        assert "saturation_pct" in metrics
        assert "snr" in metrics
        assert "mean_intensity" in metrics
