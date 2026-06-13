import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Dict, List, Optional


DATA_FILE = "users.json"


@dataclass
class User:
    username: str
    email: str
    active: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "User":
        return User(**data)


class UserManager:
    """Manage users persisted in a JSON file."""

    def __init__(self, storage_path: str = DATA_FILE):
        self.storage_path = storage_path
        self._users: Dict[str, User] = {}
        self._load()

    # ------------------------------------------------------------------ IO
    def _load(self) -> None:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self._users = {
                    uname: User.from_dict(u_dict) for uname, u_dict in raw.items()
                }
        else:
            self._users = {}

    def _save(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({u.username: u.to_dict() for u in self._users.values()}, f, indent=2)

    # ----------------------------------------------------------------- CRUD
    def add_user(self, username: str, email: str) -> User:
        if username in self._users:
            raise ValueError(f"User '{username}' already exists.")
        user = User(username=username, email=email)
        self._users[username] = user
        self._save()
        return user

    def edit_user(
        self,
        username: str,
        email: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> User:
        if username not in self._users:
            raise KeyError(f"User '{username}' not found.")
        user = self._users[username]
        if email is not None:
            user.email = email
        if active is not None:
            user.active = active
        self._save()
        return user

    def deactivate_user(self, username: str) -> User:
        return self.edit_user(username, active=False)

    def delete_user(self, username: str) -> None:
        if username not in self._users:
            raise KeyError(f"User '{username}' not found.")
        del self._users[username]
        self._save()

    def get_user(self, username: str) -> User:
        if username not in self._users:
            raise KeyError(f"User '{username}' not found.")
        return self._users[username]

    def list_users(self) -> List[User]:
        return list(self._users.values())

    # --------------------------------------------------------------- CLI helpers
    def cli_add(self, args: argparse.Namespace) -> None:
        self.add_user(args.username, args.email)
        print(f"Added user '{args.username}'.")

    def cli_edit(self, args: argparse.Namespace) -> None:
        active = None
        if args.active is not None:
            active = args.active.lower() in ("true", "1", "yes")
        self.edit_user(args.username, email=args.email, active=active)
        print(f"Edited user '{args.username}'.")

    def cli_deactivate(self, args: argparse.Namespace) -> None:
        self.deactivate_user(args.username)
        print(f"Deactivated user '{args.username}'.")

    def cli_delete(self, args: argparse.Namespace) -> None:
        self.delete_user(args.username)
        print(f"Deleted user '{args.username}'.")

    def cli_list(self, _: argparse.Namespace) -> None:
        users = self.list_users()
        if not users:
            print("No users.")
            return
        for u in users:
            status = "active" if u.active else "inactive"
            print(f"{u.username}: {u.email} ({status})")

    # --------------------------------------------------------------- Web server
    def run_server(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        manager = self

        class Handler(BaseHTTPRequestHandler):
            def _render_form(self) -> str:
                return """
                <h2>Add User</h2>
                <form method="POST" action="/add">
                  Username: <input name="username"><br>
                  Email: <input name="email"><br>
                  <input type="submit" value="Add">
                </form>
                <hr>
                """

            def _render_user_table(self) -> str:
                rows = ""
                for u in manager.list_users():
                    rows += f"<tr><td>{u.username}</td><td>{u.email}</td><td>{'yes' if u.active else 'no'}</td>"
                    rows += f"""<td>
                        <form style="display:inline" method="POST" action="/deactivate">
                          <input type="hidden" name="username" value="{u.username}">
                          <input type="submit" value="Deactivate">
                        </form>
                        <form style="display:inline" method="POST" action="/delete">
                          <input type="hidden" name="username" value="{u.username}">
                          <input type="submit" value="Delete">
                        </form>
                      </td></tr>"""
                return f"""
                <h2>Current Users</h2>
                <table border="1"><tr><th>Username</th><th>Email</th><th>Active</th><th>Actions</th></tr>{rows}</table>
                """

            def _respond(self, html: str, code: int = 200) -> None:
                self.send_response(code)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))

            def do_GET(self):
                if self.path != "/":
                    self.send_error(404, "Not found")
                    return
                html = f"""
                <html><head><title>Mail Haven</title></head><body>
                {self._render_form()}
                {self._render_user_table()}
                </body></html>
                """
                self._respond(html)

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode()
                data = parse_qs(body)
                path = urlparse(self.path).path

                try:
                    if path == "/add":
                        manager.add_user(
                            data["username"][0].strip(), data["email"][0].strip()
                        )
                    elif path == "/deactivate":
                        manager.deactivate_user(data["username"][0].strip())
                    elif path == "/delete":
                        manager.delete_user(data["username"][0].strip())
                    else:
                        self.send_error(404, "Unknown action")
                        return
                    self.send_response(303)
                    self.send_header("Location", "/")
                    self.end_headers()
                except Exception as e:
                    self.send_error(400, str(e))

        server = HTTPServer((host, port), Handler)
        print(f"Serving on http://{host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")
            server.server_close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mail_haven")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = subparsers.add_parser("add", help="Add a new user")
    p_add.add_argument("--username", required=True)
    p_add.add_argument("--email", required=True)

    # edit
    p_edit = subparsers.add_parser("edit", help="Edit an existing user")
    p_edit.add_argument("--username", required=True)
    p_edit.add_argument("--email")
    p_edit.add_argument("--active", help="true/false")

    # deactivate
    p_deact = subparsers.add_parser(
        "deactivate", help="Deactivate a user (set active=False)"
    )
    p_deact.add_argument("--username", required=True)

    # delete
    p_del = subparsers.add_parser("delete", help="Delete a user")
    p_del.add_argument("--username", required=True)

    # list
    subparsers.add_parser("list", help="List all users")

    # runserver
    p_srv = subparsers.add_parser("runserver", help="Start a simple web UI")
    p_srv.add_argument("--host", default="0.0.0.0")
    p_srv.add_argument("--port", type=int, default=8000)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    manager = UserManager()

    if args.command == "add":
        manager.cli_add(args)
    elif args.command == "edit":
        manager.cli_edit(args)
    elif args.command == "deactivate":
        manager.cli_deactivate(args)
    elif args.command == "delete":
        manager.cli_delete(args)
    elif args.command == "list":
        manager.cli_list(args)
    elif args.command == "runserver":
        manager.run_server(host=args.host, port=args.port)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
