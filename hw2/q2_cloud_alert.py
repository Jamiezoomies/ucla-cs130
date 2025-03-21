import time
import random
import logging
from datetime import datetime, timedelta
import numpy as np

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Alert severity and thresholds
ALERT_THRESHOLDS = {
    "P0": {"latency": 2000, "failure_rate": 10, "interval": 2},
    "P1": {"latency": 1000, "failure_rate": 5, "interval": 12},
    "P2": {"latency": 500, "failure_rate": 2, "interval": 48},
}

# Emails
target_email = "team@example.com"
skip_level_email = "boss@example.com"

active_alerts = {}
log_records = []
log_retention_days = 90

def generate_metrics():
    latency = np.random.poisson(750)
    failure_rate = np.random.poisson(3) / 100
    return latency, failure_rate * 100

def determine_alert(latency, failure_rate):
    for severity, params in ALERT_THRESHOLDS.items():
        if latency > params["latency"] or failure_rate > params["failure_rate"]:
            return severity
    return None

def send_email(recipient, subject, message):
    logging.info(f"{subject} - {message} <EMAIL to {recipient}>")

def log_system_status(latency, failure_rate):
    log_records.append((datetime.now(), latency, failure_rate))
    logging.info(f"INFO: Latency: {latency}ms, Failure Rate: {failure_rate:.2f}%")

def resolve_alerts():
    if active_alerts:
        for alert_id in list(active_alerts.keys()):
            logging.info(f"INFO: Commit {random.randint(1000, 9999)} submitted")
            del active_alerts[alert_id]
            logging.info(f"INFO: Alert {alert_id} resolved.")

def check_alerts():
    now = datetime.now()
    for alert_id, alert_data in list(active_alerts.items()):
        severity, timestamp, notified, escalation_time = alert_data
        resend_interval = ALERT_THRESHOLDS[severity]["interval"]
        
        if now >= timestamp + timedelta(hours=resend_interval) and not notified:
            logging.info(f"ALERT: Resending {severity} alert (Still unresolved)")
            active_alerts[alert_id] = (severity, now, False, escalation_time)
        
        if now >= escalation_time:
            logging.info(f"ESCALATION: {severity} alert unresolved for too long. Send a notification to skip-level boss.")
            del active_alerts[alert_id]

def clean_old_logs():
    cutoff = datetime.now() - timedelta(days=log_retention_days)
    global log_records
    log_records = [record for record in log_records if record[0] > cutoff]

def run_monitoring_system(duration_minutes=60):
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < duration_minutes * 60:
        latency, failure_rate = generate_metrics()
        log_system_status(latency, failure_rate)
        
        alert_severity = determine_alert(latency, failure_rate)
        if alert_severity:
            alert_id = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            if alert_id not in active_alerts:
                logging.info(f"{alert_id} {alert_severity} Alert Triggered.")
                send_email(target_email, f"ALERT: {alert_severity} Triggered", "Immediate action required.")
                escalation_time = datetime.now() + timedelta(hours=5 * ALERT_THRESHOLDS[alert_severity]["interval"])
                active_alerts[alert_id] = (alert_severity, datetime.now(), False, escalation_time)
        
        # resolving an issue simulation
        if random.random() < 0.3:
            resolve_alerts()
        
        check_alerts()
        clean_old_logs()
        
        time.sleep(10)

if __name__ == "__main__":
    run_monitoring_system(duration_minutes=60)
