import os
import tempfile

import pytest

from mail_haven import UserManager, User


@pytest.fixture
def fresh_manager(tmp_path):
    """Create a UserManager that uses a temporary JSON file."""
    storage = os.path.join(tmp_path, "users.json")
    return UserManager(storage_path=storage)


def test_add_user(fresh_manager):
    u = fresh_manager.add_user("alice", "alice@example.com")
    assert isinstance(u, User)
    assert u.username == "alice"
    assert u.email == "alice@example.com"
    assert u.active is True

    # Adding same username should raise
    with pytest.raises(ValueError):
        fresh_manager.add_user("alice", "alice2@example.com")


def test_edit_user(fresh_manager):
    fresh_manager.add_user("bob", "bob@example.com")
    fresh_manager.edit_user("bob", email="bob@new.com")
    u = fresh_manager.get_user("bob")
    assert u.email == "bob@new.com"
    assert u.active is True

    fresh_manager.edit_user("bob", active=False)
    u = fresh_manager.get_user("bob")
    assert u.active is False

    with pytest.raises(KeyError):
        fresh_manager.edit_user("nonexistent", email="x")


def test_deactivate_and_delete(fresh_manager):
    fresh_manager.add_user("carol", "c@example.com")
    fresh_manager.deactivate_user("carol")
    assert fresh_manager.get_user("carol").active is False

    fresh_manager.delete_user("carol")
    with pytest.raises(KeyError):
        fresh_manager.get_user("carol")

    # Deleting non‑existent user raises
    with pytest.raises(KeyError):
        fresh_manager.delete_user("carol")


def test_list_users(fresh_manager):
    assert fresh_manager.list_users() == []
    fresh_manager.add_user("dave", "d@example.com")
    fresh_manager.add_user("eve", "e@example.com")
    usernames = {u.username for u in fresh_manager.list_users()}
    assert usernames == {"dave", "eve"}
