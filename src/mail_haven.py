import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Metric:
    name: str
    value: float
    timestamp: datetime

class MailHaven:
    def __init__(self):
        self.metrics = []
        self.logs = []

    def collect_metrics(self):
        # Simulate collecting metrics
        self.metrics.append(Metric("cpu_usage", 50.0, datetime.now()))
        self.metrics.append(Metric("memory_usage", 75.0, datetime.now()))

    def collect_logs(self):
        # Simulate collecting logs
        self.logs.append({"level": "INFO", "message": "Server started", "timestamp": datetime.now()})
        self.logs.append({"level": "WARNING", "message": "Low disk space", "timestamp": datetime.now()})

    def display_metrics(self):
        print("Metrics:")
        for metric in self.metrics:
            print(f"{metric.name}: {metric.value} at {metric.timestamp}")

    def search_logs(self, query):
        results = [log for log in self.logs if query in log["message"]]
        return results

    def trigger_alerts(self):
        critical_logs = [log for log in self.logs if log["level"] == "ERROR"]
        if critical_logs:
            print("Critical issue detected:")
            for log in critical_logs:
                print(f"{log['level']}: {log['message']} at {log['timestamp']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--search", type=str)
    parser.add_argument("--alert", action="store_true")
    args = parser.parse_args()

    mail_haven = MailHaven()

    if args.collect:
        mail_haven.collect_metrics()
        mail_haven.collect_logs()

    if args.display:
        mail_haven.display_metrics()

    if args.search:
        results = mail_haven.search_logs(args.search)
        print("Search results:")
        for result in results:
            print(f"{result['level']}: {result['message']} at {result['timestamp']}")

    if args.alert:
        mail_haven.trigger_alerts()

if __name__ == "__main__":
    main()
