import pytest
from persistence import AccessControlData


def test_authenticate_success(model: AccessControlData):
    username, password = "Bob", "somePassword1"
    model.add_user(username, password)

    assert model.users == { username : password }
    assert model.authenticate(username, password)


def test_authenticate_failure(model: AccessControlData):
    username, password = "Bob", "somePassword1"
    model.add_user(username, password)

    assert model.users == { username : password }
    assert model.authenticate(username, "incorrect password") == False


def test_authenticate_invalid_username(model: AccessControlData):
    with pytest.raises(ValueError):
        model.authenticate("", "pass")
    
    with pytest.raises(ValueError):
        model.authenticate(None, "pass")


def test_authenticate_invalid_password(model: AccessControlData):
    with pytest.raises(ValueError):
        model.authenticate("Bob", "")
    
    with pytest.raises(ValueError):
        model.authenticate("Bob", None)


def test_authenticate_nonexistent_user(model: AccessControlData):
    model.add_user("user1", "password1")
    model.add_user("user2", "password2")
    model.add_user("user3", "password3")

    assert model.users == {
        "user1": "password1",
        "user2": "password2",
        "user3": "password3",
    }

    with pytest.raises(KeyError):
        model.authenticate("user4", "password4")