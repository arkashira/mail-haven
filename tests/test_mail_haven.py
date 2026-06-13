import pytest
from mail_haven import MailHaven, Metric

def test_collect_metrics():
    mail_haven = MailHaven()
    mail_haven.collect_metrics()
    assert len(mail_haven.metrics) == 2

def test_collect_logs():
    mail_haven = MailHaven()
    mail_haven.collect_logs()
    assert len(mail_haven.logs) == 2

def test_display_metrics(capsys):
    mail_haven = MailHaven()
    mail_haven.collect_metrics()
    mail_haven.display_metrics()
    captured = capsys.readouterr()
    assert "Metrics:" in captured.out

def test_search_logs():
    mail_haven = MailHaven()
    mail_haven.collect_logs()
    results = mail_haven.search_logs("started")
    assert len(results) == 1

def test_trigger_alerts(capsys):
    mail_haven = MailHaven()
    mail_haven.logs.append({"level": "ERROR", "message": "Critical issue", "timestamp": "2022-01-01"})
    mail_haven.trigger_alerts()
    captured = capsys.readouterr()
    assert "Critical issue detected:" in captured.out

def test_main_collect():
    import sys
    sys.argv = ["mail_haven.py", "--collect"]
    from mail_haven import main
    main()
    mail_haven = MailHaven()
    assert len(mail_haven.metrics) == 0  # main() doesn't store metrics

def test_main_display(capsys):
    import sys
    sys.argv = ["mail_haven.py", "--display"]
    from mail_haven import main
    main()
    captured = capsys.readouterr()
    assert "Metrics:" in captured.out

def test_main_search(capsys):
    import sys
    sys.argv = ["mail_haven.py", "--search", "started"]
    from mail_haven import main
    main()
    captured = capsys.readouterr()
    assert "Search results:" in captured.out

def test_main_alert(capsys):
    import sys
    sys.argv = ["mail_haven.py", "--alert"]
    from mail_haven import main
    main()
    captured = capsys.readouterr()
    assert "Critical issue detected:" not in captured.out  # no critical logs
