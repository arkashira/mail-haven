import pytest
from mail_haven import MailHaven, EmailServerMetrics
import logging
import tempfile
import os

@pytest.fixture
def log_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        yield f.name
    os.remove(f.name)

def test_collect_metrics():
    mail_haven = MailHaven('test.log')
    metrics = mail_haven.collect_metrics()
    assert isinstance(metrics, EmailServerMetrics)
    assert metrics.cpu_usage == 50.0
    assert metrics.memory_usage == 75.0
    assert metrics.disk_usage == 25.0

def test_log_metrics(log_file):
    mail_haven = MailHaven(log_file)
    metrics = EmailServerMetrics(50.0, 75.0, 25.0)
    mail_haven.log_metrics(metrics)
    with open(log_file, 'r') as f:
        log_line = f.read()
    assert 'CPU usage: 50.0%, Memory usage: 75.0%, Disk usage: 25.0%' in log_line

def test_trigger_alert():
    mail_haven = MailHaven('test.log')
    metrics = EmailServerMetrics(90.0, 75.0, 25.0)
    assert mail_haven.trigger_alert(metrics)
    metrics = EmailServerMetrics(50.0, 75.0, 25.0)
    assert not mail_haven.trigger_alert(metrics)

def test_main(log_file):
    import sys
    sys.argv = ['mail_haven.py', '--log_file', log_file]
    from mail_haven import main
    main()
    with open(log_file, 'r') as f:
        log_line = f.read()
    assert 'CPU usage: 50.0%, Memory usage: 75.0%, Disk usage: 25.0%' in log_line
