import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmailServerMetrics:
    cpu_usage: float
    memory_usage: float
    disk_usage: float

class MailHaven:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger('mail_haven')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(log_file)
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(self.handler)

    def collect_metrics(self):
        # Simulate collecting metrics
        cpu_usage = 50.0
        memory_usage = 75.0
        disk_usage = 25.0
        return EmailServerMetrics(cpu_usage, memory_usage, disk_usage)

    def log_metrics(self, metrics):
        self.logger.info(f'CPU usage: {metrics.cpu_usage}%, Memory usage: {metrics.memory_usage}%, Disk usage: {metrics.disk_usage}%')

    def trigger_alert(self, metrics):
        if metrics.cpu_usage > 80 or metrics.memory_usage > 90 or metrics.disk_usage > 95:
            self.logger.warning('Critical issue detected!')
            return True
        return False

def main():
    parser = argparse.ArgumentParser(description='Mail Haven')
    parser.add_argument('--log_file', default='mail_haven.log', help='Log file path')
    args = parser.parse_args()
    mail_haven = MailHaven(args.log_file)
    metrics = mail_haven.collect_metrics()
    mail_haven.log_metrics(metrics)
    mail_haven.trigger_alert(metrics)

if __name__ == '__main__':
    main()
