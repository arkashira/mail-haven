from mail_haven import generate_config, deploy_email_server, EmailServerConfig
import pytest
from io import StringIO
import sys

def test_generate_config() -> None:
    domain = "example.com"
    port = 25
    username = "user"
    password = "pass"
    expected_config = {
        "domain": domain,
        "port": port,
        "username": username,
        "password": password
    }
    assert generate_config(domain, port, username, password) == expected_config

def test_deploy_email_server(capsys: pytest.CaptureFixture) -> None:
    config = {
        "domain": "example.com",
        "port": 25,
        "username": "user",
        "password": "pass"
    }
    deploy_email_server(config)
    captured = capsys.readouterr()
    assert "Deploying email server with config" in captured.out

def test_main() -> None:
    sys.argv = ["mail_haven.py", "--domain", "example.com", "--port", "25", "--username", "user", "--password", "pass"]
    import contextlib
    f = StringIO()
    with contextlib.redirect_stdout(f):
        from mail_haven import main
        main()
    assert "Deploying email server with config" in f.getvalue()

def test_main_missing_args() -> None:
    sys.argv = ["mail_haven.py"]
    with pytest.raises(SystemExit):
        from mail_haven import main
        main()
