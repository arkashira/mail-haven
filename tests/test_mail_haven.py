import pytest
import os
from mail_haven import EmailServerConfig, generate_config, deploy_email_server

def test_generate_config():
    config = generate_config()
    assert config.domain == "example.com"
    assert config.username == "admin"
    assert config.password == "password"
    assert config.port == 25

def test_deploy_email_server(tmp_path):
    config = EmailServerConfig("example.com", "admin", "password", 25)
    deploy_email_server(config)
    assert os.path.exists("email_server_config.json")

def test_main(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHONPATH", "src")
    import sys
    sys.argv = ["mail_haven.py", "--domain", "example.com", "--username", "admin", "--password", "password", "--port", "25"]
    from mail_haven import main
    main()
    assert os.path.exists("email_server_config.json")

def test_main_with_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHONPATH", "src")
    import sys
    sys.argv = ["mail_haven.py"]
    from mail_haven import main
    main()
    assert os.path.exists("email_server_config.json")
