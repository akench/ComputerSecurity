import pytest
from persistence import AccessControlData

""" Testing all functionality for user groups """

def test_add_user_to_group_success(model: AccessControlData):
    model.add_user("Bob", "greatPassword123#")
    model.add_user_to_group("Bob", "people")

    assert model.user_to_groups["Bob"] == { "people" }
    assert model.get_users_in_group("people") == { "Bob" }


def test_add_user_to_group_redundantly(model: AccessControlData):
    # Adding a user to the same group twice should not result
    # in redundant storage of the user in that group
    model.add_user("Bob", "greatPassword123#")
    model.add_user_to_group("Bob", "people")
    model.add_user_to_group("Bob", "humans")
    model.add_user_to_group("Bob", "people")

    assert model.user_to_groups["Bob"] == { "people", "humans" }
    assert model.get_users_in_group("people") == { "Bob" }


def test_add_user_to_group_invalid_inputs(model: AccessControlData):
    with pytest.raises(ValueError):
        model.add_user("", "usergroup")

    with pytest.raises(ValueError):
        model.add_user(None, "usergroup")

    with pytest.raises(ValueError):
        model.add_user("user", "")

    with pytest.raises(ValueError):
        model.add_user("user", None)


def test_add_user_to_group_nonexistent_user(model: AccessControlData):
    with pytest.raises(KeyError):
        model.add_user_to_group("Bob", "humans")


def test_add_multiple_users_to_groups(model: AccessControlData):
    # Create dummy users
    model.add_user("Bob", "password")
    model.add_user("Jane Doe", "password")
    model.add_user("John Doe", "password")
    model.add_user("Winnie the Pooh", "password")
    model.add_user("Tigger", "password")

    # Add users to their respective groups
    model.add_user_to_group("Bob",             "humans")
    model.add_user_to_group("Bob",             "workers")
    model.add_user_to_group("Jane Doe",        "humans")
    model.add_user_to_group("John Doe",        "humans")
    model.add_user_to_group("John Doe",        "workers")
    model.add_user_to_group("Winnie the Pooh", "humans") # ?
    model.add_user_to_group("Winnie the Pooh", "animals")
    model.add_user_to_group("Tigger",          "animals")

    # Ensure all groups are as expected
    assert model.get_users_in_group("humans") == \
        { "Bob", "Jane Doe", "John Doe", "Winnie the Pooh" }
    assert model.get_users_in_group("workers") == \
        { "Bob", "John Doe" }
    assert model.get_users_in_group("animals") == \
        { "Winnie the Pooh", "Tigger" }
    assert not model.get_users_in_group("nonexistent_group")


""" Testing all functionality for object groups """

def test_add_object_to_group_success(model: AccessControlData):
    model.add_object_to_group("stick", "wood")

    assert model.object_to_group["stick"] == "wood"
    assert model.get_objects_in_group("wood") == { "stick" }


def test_add_object_to_group_redundantly(model: AccessControlData):
    # We only support one group per object. Adding an object to
    # two groups (whether they are the same or not), should result
    # in an error
    model.add_object_to_group("stick", "wood")

    with pytest.raises(KeyError):
        model.add_object_to_group("stick", "wood")


def test_add_object_to_group_invalid_inputs(model: AccessControlData):
    with pytest.raises(ValueError):
        model.add_object_to_group("", "objectgroup")

    with pytest.raises(ValueError):
        model.add_object_to_group(None, "objectgroup")

    with pytest.raises(ValueError):
        model.add_object_to_group("object", "")

    with pytest.raises(ValueError):
        model.add_object_to_group("object", None)


def test_add_multiple_objects_to_groups(model: AccessControlData):
    # Add users to their respective groups
    model.add_object_to_group("table",  "furniture")
    model.add_object_to_group("chair",  "furniture")
    model.add_object_to_group("fork",   "utensils")
    model.add_object_to_group("spoon",  "utensils")
    model.add_object_to_group("plates", "utensils")
    model.add_object_to_group("pencil", "stationery")
    model.add_object_to_group("paper",  "stationery")
    model.add_object_to_group("eraser", "stationery")

    # Ensure all groups are as expected
    assert model.get_objects_in_group("furniture") == \
        { "table", "chair" }
    assert model.get_objects_in_group("utensils") == \
        { "fork", "spoon", "plates" }
    assert model.get_objects_in_group("stationery") == \
        { "pencil", "paper", "eraser" }
    assert not model.get_objects_in_group("nonexistent_group")