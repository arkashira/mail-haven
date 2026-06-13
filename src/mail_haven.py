import argparse
import json
import os
from dataclasses import dataclass

@dataclass
class EmailServerConfig:
    domain: str
    username: str
    password: str
    port: int

def generate_config():
    return EmailServerConfig(
        domain="example.com",
        username="admin",
        password="password",
        port=25
    )

def deploy_email_server(config):
    # Simulate deployment by creating a config file
    with open("email_server_config.json", "w") as f:
        json.dump(config.__dict__, f)

def main():
    parser = argparse.ArgumentParser(description="Deploy an email server")
    parser.add_argument("--domain", help="Domain for the email server")
    parser.add_argument("--username", help="Username for the email server")
    parser.add_argument("--password", help="Password for the email server")
    parser.add_argument("--port", type=int, help="Port for the email server")
    args = parser.parse_args()
    if args.domain and args.username and args.password and args.port:
        config = EmailServerConfig(args.domain, args.username, args.password, args.port)
    else:
        config = generate_config()
    deploy_email_server(config)

if __name__ == "__main__":
    main()
