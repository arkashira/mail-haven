import argparse
import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class EmailServerConfig:
    domain: str
    port: int
    username: str
    password: str

def generate_config(domain: str, port: int, username: str, password: str) -> Dict:
    return {
        "domain": domain,
        "port": port,
        "username": username,
        "password": password
    }

def deploy_email_server(config: Dict) -> None:
    print(f"Deploying email server with config: {json.dumps(config)}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy an email server")
    parser.add_argument("--domain", required=True, help="Email server domain")
    parser.add_argument("--port", type=int, default=25, help="Email server port")
    parser.add_argument("--username", required=True, help="Email server username")
    parser.add_argument("--password", required=True, help="Email server password")
    args = parser.parse_args()

    config = generate_config(args.domain, args.port, args.username, args.password)
    deploy_email_server(config)

if __name__ == "__main__":
    main()
