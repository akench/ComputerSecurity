import pytest
from persistence import AccessControlData


def test_create_user(model: AccessControlData):
    username, password = "Bob", "greatPassword123#"
    model.add_user(username, password)

    assert model.users == { username: password }


def test_create_user_invalid_username(model: AccessControlData):
    with pytest.raises(ValueError):
        model.add_user("", "somePassword")

    with pytest.raises(ValueError):
        model.add_user(None, "somePassword")


def test_create_user_invalid_password(model: AccessControlData):
    with pytest.raises(ValueError):
        model.add_user("someUsername", "")

    with pytest.raises(ValueError):
        model.add_user("someUsername", None)


def test_create_user_existing_user(model: AccessControlData):
    model.add_user("Bob", "pass")

    with pytest.raises(KeyError):
        model.add_user("Bob", "otherPassword")