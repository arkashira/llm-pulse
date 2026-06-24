from llm_pulse import LLM_Pulse, Metric, Issue
import json
from datetime import datetime

def test_add_metric():
    llm_pulse = LLM_Pulse()
    metric = Metric("cpu_usage", 50.0, datetime.now())
    llm_pulse.add_metric(metric)
    assert len(llm_pulse.get_metrics()) == 1

def test_add_issue():
    llm_pulse = LLM_Pulse()
    issue = Issue("high_cpu_usage", "CPU usage is high", datetime.now())
    llm_pulse.add_issue(issue)
    assert len(llm_pulse.get_issues()) == 1

def test_filter_metrics():
    llm_pulse = LLM_Pulse()
    metric1 = Metric("cpu_usage", 50.0, datetime.now())
    metric2 = Metric("memory_usage", 30.0, datetime.now())
    llm_pulse.add_metric(metric1)
    llm_pulse.add_metric(metric2)
    filtered_metrics = llm_pulse.filter_metrics("cpu_usage")
    assert len(filtered_metrics) == 1
    assert filtered_metrics[0].name == "cpu_usage"

def test_filter_issues():
    llm_pulse = LLM_Pulse()
    issue1 = Issue("high_cpu_usage", "CPU usage is high", datetime.now())
    issue2 = Issue("high_memory_usage", "Memory usage is high", datetime.now())
    llm_pulse.add_issue(issue1)
    llm_pulse.add_issue(issue2)
    filtered_issues = llm_pulse.filter_issues("high_cpu_usage")
    assert len(filtered_issues) == 1
    assert filtered_issues[0].name == "high_cpu_usage"

def test_to_json():
    llm_pulse = LLM_Pulse()
    metric = Metric("cpu_usage", 50.0, datetime.now())
    issue = Issue("high_cpu_usage", "CPU usage is high", datetime.now())
    llm_pulse.add_metric(metric)
    llm_pulse.add_issue(issue)
    json_data = llm_pulse.to_json()
    data = json.loads(json_data)
    assert len(data["metrics"]) == 1
    assert len(data["issues"]) == 1
