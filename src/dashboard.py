import json
from dataclasses import dataclass
from typing import List

@dataclass
class API:
    name: str
    performance_data: dict
    alerts: List[str]

class Dashboard:
    def __init__(self):
        self.apis = []

    def add_api(self, api: API):
        self.apis.append(api)

    def get_realtime_performance_data(self):
        return {api.name: api.performance_data for api in self.apis}

    def get_alerts(self):
        alerts = []
        for api in self.apis:
            for alert in api.alerts:
                alerts.append((api.name, alert))
        return alerts

    def is_responsive(self, device: str):
        # Simulate responsiveness check
        return device in ["desktop", "mobile", "tablet"]

    def is_accessible(self, device: str):
        # Simulate accessibility check
        return device in ["desktop", "mobile", "tablet"]
