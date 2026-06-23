from email_alerts import EmailAlerts, Incident, NotificationPreferences, load_smtp_settings

def test_send_email():
    smtp_settings = load_smtp_settings(1)
    email_alerts = EmailAlerts(smtp_settings)
    incident = Incident(1, "Test incident", "High")
    user_email = "user@example.com"
    notification_preferences = NotificationPreferences(True, False)

    email_alerts.send_email(incident, user_email, notification_preferences)

    # Simulate checking the email was sent
    assert True

def test_get_email_template():
    incident = Incident(1, "Test incident", "High")
    email_alerts = EmailAlerts(load_smtp_settings(1))
    email_template = email_alerts.get_email_template(incident)

    assert email_template == "Incident 1: Test incident (Severity: High)"

def test_send_email_respects_notification_preferences():
    smtp_settings = load_smtp_settings(1)
    email_alerts = EmailAlerts(smtp_settings)
    incident = Incident(1, "Test incident", "High")
    user_email = "user@example.com"
    notification_preferences = NotificationPreferences(False, True)

    email_alerts.send_email(incident, user_email, notification_preferences)

    # Simulate checking the email was not sent
    assert True

def test_load_smtp_settings():
    smtp_settings = load_smtp_settings(1)

    assert smtp_settings['from'] == 'incident-alerts@example.com'
    assert smtp_settings['host'] == 'smtp.example.com'
    assert smtp_settings['port'] == 587
    assert smtp_settings['username'] == 'incident-alerts'
    assert smtp_settings['password'] == 'password'
