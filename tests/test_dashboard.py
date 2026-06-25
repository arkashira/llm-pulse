import pytest
from dashboard import API, Dashboard

def test_get_realtime_performance_data():
    dashboard = Dashboard()
    api1 = API("API 1", {"status": "ok"}, [])
    api2 = API("API 2", {"status": "error"}, [])
    dashboard.add_api(api1)
    dashboard.add_api(api2)
    assert dashboard.get_realtime_performance_data() == {
        "API 1": {"status": "ok"},
        "API 2": {"status": "error"}
    }

def test_get_alerts():
    dashboard = Dashboard()
    api1 = API("API 1", {}, ["alert 1", "alert 2"])
    api2 = API("API 2", {}, ["alert 3"])
    dashboard.add_api(api1)
    dashboard.add_api(api2)
    assert dashboard.get_alerts() == [
        ("API 1", "alert 1"),
        ("API 1", "alert 2"),
        ("API 2", "alert 3")
    ]

def test_is_responsive():
    dashboard = Dashboard()
    assert dashboard.is_responsive("desktop")
    assert not dashboard.is_responsive("unknown")

def test_is_accessible():
    dashboard = Dashboard()
    assert dashboard.is_accessible("mobile")
    assert not dashboard.is_accessible("unknown")

def test_add_api():
    dashboard = Dashboard()
    api = API("API 1", {}, [])
    dashboard.add_api(api)
    assert len(dashboard.apis) == 1
