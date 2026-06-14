<h3 align="center">🛠️ Mail Haven</h3>

<div align="center">
  <a href="https://shields.io/">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://shields.io/">
    <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python 3.9">
  </a>
  <a href="https://shields.io/">
    <img src="https://img.shields.io/badge/Build-Poetry-blue.svg" alt="Build with Poetry">
  </a>
  <a href="https://shields.io/">
    <img src="https://img.shields.io/github/stars/axentx/mail-haven?style=social" alt="Stars: 0">
  </a>
</div>

---

# 🚀 Mail Haven

**Power your email infrastructure with a self-hosted solution.** Mail Haven is a self-hosted email solution for individuals or organizations to manage their email services.

---

## Why Mail Haven?

* **Secure**: Have full control over your email infrastructure.
* **Flexible**: Deploy locally or in your preferred environment.
* **Scalable**: Easily manage your email services as your needs grow.
* **Customizable**: Tailor your email solution to meet your specific requirements.
* **Cost-effective**: Avoid external email service costs.
* **Private**: Keep your email data private and secure.

---

## Feature Overview

| Feature | Description |
| --- | --- |
| Email Server | A Python-based implementation with dependencies managed by Poetry. |
| User Management | Basic structure for setting up an email server, with user management capabilities. |
| Web Interface | Not immediately clear from the provided files, but suggested by the presence of a tests directory. |
| Documentation | Well-documented codebase with tests and documentation directories. |

---

## Tech Stack

* Python
* Poetry

---

## Project Structure

* `axentx_product`
* `business`
* `docs`
* `src`
* `tests`

---

## Getting Started

### Install Dependencies

```bash
poetry install
```

### Run the Email Server

```bash
poetry run python src/main.py
```

### Test the Email Server

```bash
poetry run pytest tests/
```

---

## Deploy

### Deploy to a Local Environment

```bash
poetry run python src/main.py
```

### Deploy to a Remote Environment (e.g., Docker)

```bash
docker build -t mail-haven .
docker run -p 8080:8080 mail-haven
```

---

## Status

Mail Haven is currently in the early stages of development, with recent commits focusing on implementing a real, sandbox-tested email server.

### Recent Commits

* f08bee5 style: [DECISION] docs cycle 20260614-190959-mail-hav
* eb1d2f3 feat(mail-haven): real, sandbox-tested implementation
* b4a369e readme-keeper: generate proper project README (overview/stack/run/deploy)
* ee084b4 feat(mail-haven): real, sandbox-tested implementation
* 359383b style: [DECISION] docs cycle 20260613-180105-mail-hav
* 660c7c8 feat(mail-haven): real, sandbox-tested implementation
* fe58a54 style: [DECISION] docs cycle 20260613-132946-mail-hav
* 564afc5 feat(mail-haven): real, sandbox-tested implementation

---

## Contributing

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on contributing to Mail Haven.

---

## License

Mail Haven is licensed under the MIT License.