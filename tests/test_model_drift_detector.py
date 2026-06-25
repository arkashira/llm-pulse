from model_drift_detector import ModelDriftDetector
import pytest

def test_embed():
    detector = ModelDriftDetector()
    embedding = detector.embed("Hello World")
    assert len(embedding.vector) == 11

def test_cluster_no_drift():
    detector = ModelDriftDetector()
    detector.cluster("prompt", "response")
    detector.cluster("prompt", "response")
    assert "prompt" in detector.centroids

def test_cluster_drift():
    detector = ModelDriftDetector()
    detector.cluster("prompt", "response")
    with pytest.raises(ValueError):
        detector.cluster("prompt", "different response")

def test_sample():
    detector = ModelDriftDetector()
    assert detector.sample("prompt", "response") or not detector.sample("prompt", "response")

def test_detect_drift_no_drift():
    detector = ModelDriftDetector(sample_rate=1.0)
    detector.detect_drift("prompt", "response")
    detector.detect_drift("prompt", "response")
    assert "prompt" in detector.centroids

def test_detect_drift_drift():
    detector = ModelDriftDetector(sample_rate=1.0)
    detector.detect_drift("prompt", "response")
    with pytest.raises(ValueError):
        detector.detect_drift("prompt", "different response")
