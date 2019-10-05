import pytest
from persistence import AccessControlData


################################
### CREATION OF PERMISSIONS  ###
################################

def test_add_access_invalid_param(model: AccessControlData):
    with pytest.raises(ValueError):
        model.add_access("", "valid_user_group")

    with pytest.raises(ValueError):
        model.add_access("valid_op", "")

    with pytest.raises(ValueError):
        model.add_access("", "")


def test_add_access_success(model: AccessControlData):
    model.add_access("read", "humans", "books")
    model.add_access("walk", "humans", None)
    assert model.permissions == \
        { ("read", "humans", "books"), ("walk", "humans", None) }


def test_add_access_duplicate_permissions(model: AccessControlData):
    model.add_access("read", "humans", "books")

    # The permission already exists, so it will raise an error
    with pytest.raises(ValueError):
        model.add_access("read", "humans", "books")
        

def test_add_access_duplicate_permissions_all(model: AccessControlData):
    model.add_access("read", "humans", "books")
    
    with pytest.raises(ValueError):
        model.add_access("read", "humans", None)


def test_add_access_duplicate_permissions_all_2(model: AccessControlData):
    model.add_access("read", "humans", None)
    
    with pytest.raises(ValueError):
        model.add_access("read", "humans", "books")


#############################
### ACCESS OF PERMISSIONS ###
#############################

def test_can_access_invalid_params(model: AccessControlData):
    with pytest.raises(ValueError):
        model.can_access("", "username")

    with pytest.raises(ValueError):
        model.can_access("operation", "")

    with pytest.raises(ValueError):
        model.can_access("", "")


def test_can_access_invalid_user(model: AccessControlData):
    with pytest.raises(KeyError):
        model.can_access("operation", "invalid user")


def test_can_access_invalid_object(model: AccessControlData):
    model.add_user("Bob", "password")
    
    with pytest.raises(KeyError):
        model.can_access("operation", "Bob", "invalid object")


def test_can_access_success(model: AccessControlData):
    model.add_user("bob", "pass")
    model.add_user_to_group("bob", "humans")
    model.add_object_to_group("Handmade's Tail", "books")
    model.add_access("read", "humans", "books")

    assert model.can_access("read", "bob", "Handmade's Tail")


def test_can_access_empty_permissions(model: AccessControlData):
    model.add_user("bob", "pass")
    model.add_user_to_group("bob", "humans")
    model.add_object_to_group("Handmade's Tail", "books")

    assert not model.permissions
    assert not model.can_access("read", "bob", "Handmade's Tail")


def test_can_access_failure(model: AccessControlData):
    model.add_user("bob", "pass")
    model.add_user_to_group("bob", "humans")
    model.add_object_to_group("Handmade's Tail", "books")
    model.add_access("read", "humans", "books")

    assert not model.can_access("write", "bob", "Handmade's Tail")


def test_can_access_success_null_object(model: AccessControlData):
    model.add_user("bob", "pass")
    model.add_user_to_group("bob", "humans")
    model.add_object_to_group("Handmade's Tail", "books")
    model.add_access("read", "humans")

    assert model.can_access("read", "bob", "Handmade's Tail")
    assert not model.can_access("write", "bob", "Handmade's Tail")


def test_can_access(model: AccessControlData):
    # Create dummy users
    model.add_user("Bob", "pass")
    model.add_user("John", "pass")
    model.add_user("Robert", "pass")
    model.add_user("Winnie", "pass")
    model.add_user("Tigger", "pass")

    # Add users to groups
    model.add_user_to_group("Bob", "humans")
    model.add_user_to_group("Bob", "workers")
    model.add_user_to_group("Winnie", "bear")
    model.add_user_to_group("Winnie", "animals")
    model.add_user_to_group("Tigger", "tiger")
    model.add_user_to_group("Tigger", "animals")
    model.add_user_to_group("John", "humans")
    model.add_user_to_group("John", "student")
    model.add_user_to_group("Robert", "humans")
    model.add_user_to_group("Robert", "worker")
    model.add_user_to_group("Robert", "student")
    
    # Add objects to groups
    model.add_object_to_group("Winnie", "animals")
    model.add_object_to_group("Harry Potter", "books")
    model.add_object_to_group("Sherlock Holmes", "books")
    model.add_object_to_group("Avengers", "good movies")
    model.add_object_to_group("A serious man", "bad movies")
    model.add_object_to_group("water", "liquid")
    model.add_object_to_group("red bull", "liquid")

    # Add permissions
    model.add_access("drink", "animals", "liquid")
    model.add_access("hunt", "animals")
    model.add_access("speak", "humans")
    model.add_access("read", "humans", "books")
    model.add_access("watch", "humans", "good movies")
    model.add_access("study", "student")
    model.add_access("drink", "student", "liquid")
    model.add_access("protest", "worker")
    model.add_access("get underpaid", "worker")

    # Check for various permissions
    assert model.can_access("hunt", "Winnie")
    assert model.can_access("hunt", "Tigger", "Winnie")
    assert model.can_access("watch", "Bob", "Avengers")
    assert not model.can_access("watch", "Bob")
    assert not model.can_access("watch", "Bob", "A serious man")
    assert model.can_access("drink", "Tigger", "water")
    assert model.can_access("drink", "John", "red bull")
    assert not model.can_access("drink", "John", "Avengers")
    assert not model.can_access("watch", "John", "A serious man")
    assert model.can_access("protest", "Robert")
    assert not model.can_access("protest", "John")
    assert not model.can_access("protest", "Winnie")
    assert not model.can_access("get overpaid", "John")
    assert model.can_access("drink", "John", "water")
    assert model.can_access("drink", "Winnie", "red bull")
    assert model.can_access("speak", "Robert")
    assert not model.can_access("speak", "Tigger")
    assert model.can_access("study", "John")
    assert not model.can_access("study", "Bob")