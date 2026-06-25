import json
from dataclasses import dataclass
from typing import List
import math
import random

@dataclass
class Embedding:
    vector: List[float]

class ModelDriftDetector:
    def __init__(self, sample_rate: float = 0.1, drift_threshold: float = 0.25):
        self.sample_rate = sample_rate
        self.drift_threshold = drift_threshold
        self.centroids = {}

    def embed(self, text: str) -> Embedding:
        # Simple embedding using cosine similarity
        vector = [ord(c) / 256 for c in text]
        return Embedding(vector)

    def cluster(self, prompt: str, response: str) -> None:
        embedding = self.embed(response)
        if prompt not in self.centroids:
            self.centroids[prompt] = embedding
        else:
            centroid = self.centroids[prompt]
            dot_product = sum(a * b for a, b in zip(centroid.vector, embedding.vector))
            magnitude = math.sqrt(sum(a ** 2 for a in centroid.vector)) * math.sqrt(sum(a ** 2 for a in embedding.vector))
            similarity = dot_product / magnitude if magnitude != 0 else 0
            if 1 - similarity > self.drift_threshold:
                raise ValueError("Drift detected")

    def sample(self, prompt: str, response: str) -> bool:
        return random.random() < self.sample_rate

    def detect_drift(self, prompt: str, response: str) -> None:
        if self.sample(prompt, response):
            self.cluster(prompt, response)
