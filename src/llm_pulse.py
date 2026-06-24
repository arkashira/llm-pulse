import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Metric:
    name: str
    value: float
    timestamp: datetime

@dataclass
class Issue:
    name: str
    description: str
    timestamp: datetime

class LLM_Pulse:
    def __init__(self):
        self.metrics = []
        self.issues = []

    def add_metric(self, metric: Metric):
        self.metrics.append(metric)

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    def get_metrics(self):
        return self.metrics

    def get_issues(self):
        return self.issues

    def filter_metrics(self, name: str):
        return [metric for metric in self.metrics if metric.name == name]

    def filter_issues(self, name: str):
        return [issue for issue in self.issues if issue.name == name]

    def to_json(self):
        metrics_json = [{"name": metric.name, "value": metric.value, "timestamp": metric.timestamp.isoformat()} for metric in self.metrics]
        issues_json = [{"name": issue.name, "description": issue.description, "timestamp": issue.timestamp.isoformat()} for issue in self.issues]
        return json.dumps({"metrics": metrics_json, "issues": issues_json})

def main():
    llm_pulse = LLM_Pulse()
    metric = Metric("cpu_usage", 50.0, datetime.now())
    issue = Issue("high_cpu_usage", "CPU usage is high", datetime.now())
    llm_pulse.add_metric(metric)
    llm_pulse.add_issue(issue)
    print(llm_pulse.to_json())

if __name__ == "__main__":
    main()
