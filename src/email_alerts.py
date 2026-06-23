import json
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Dict

@dataclass
class NotificationPreferences:
    email: bool
    slack: bool

@dataclass
class Incident:
    id: int
    description: str
    severity: str

class EmailAlerts:
    def __init__(self, smtp_settings: Dict[str, str]):
        self.smtp_settings = smtp_settings

    def send_email(self, incident: Incident, user_email: str, notification_preferences: NotificationPreferences):
        if not notification_preferences.email:
            return

        msg = EmailMessage()
        msg.set_content(f" Incident {incident.id}: {incident.description} (Severity: {incident.severity})")
        msg['Subject'] = f"Incident {incident.id}: {incident.description}"
        msg['From'] = self.smtp_settings['from']
        msg['To'] = user_email

        # Simulate sending the email
        print(f"Sending email to {user_email}: {msg}")

    def get_email_template(self, incident: Incident):
        return f"Incident {incident.id}: {incident.description} (Severity: {incident.severity})"

def load_smtp_settings(org_id: int) -> Dict[str, str]:
    # Simulate loading SMTP settings from a database
    return {
        'from': 'incident-alerts@example.com',
        'host': 'smtp.example.com',
        'port': 587,
        'username': 'incident-alerts',
        'password': 'password'
    }
