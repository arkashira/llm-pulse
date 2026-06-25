# Model Drift Detector

A simple model drift detector using semantic clustering.

## Usage

1. Create a `ModelDriftDetector` instance with optional `sample_rate` and `drift_threshold` parameters.
2. Call `detect_drift` with a prompt and response to sample and cluster the response.
3. If drift is detected, a `ValueError` is raised.

## Testing

Run `pytest` to execute the tests.
