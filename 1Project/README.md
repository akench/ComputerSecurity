# Assignment 3: Implementing Access Control Mechanisms

## Group Members
- Shoumyo Chakravorti (sac384)
- Atharva Kench (ak1518)

## Note(s)
- **Extra credit**: We designed our program such that a user may be a member of multiple groups, and we would like to be graded for such cases.
- We did **not** implement our access controls such that an object may be in multiple groups. An object may only be in one group.

## Setup
There is minimal setup involved in running our project. You will only have to unzip the tarball which contains our source code and test cases:
```
tar -xzvf source.tar.gz -C Assignment3
cd Assignment3
```

## Usage
Our programs are written in Python, and therefore need to be run with the `python3` command. Here is how you would need to invoke each of our scripts once inside the unzipped source folder:
```bash
# Creating users
python3 AddUser.py username password

# Authenticating users
python3 Authenticate.py username password

# Adding users to groups
python3 AddUserToGroup.py username usergroup

# Adding objects to groups
python3 AddObjectToGroup.py objectname objectgroup

# Defining permissions
python3 AddAccess.py operation usergroup [objectgroup]

# Checking if a user has permission to access an object
python3 CanAccess.py operation usergroup [objectgroup]
```
Our scripts generate an `AccessControlData.pickle` file to store all data needed to implement the access controls. If you happen to incorrectly input a test case, you can simply delete this `.pickle` file to start over (although you will have to redo the steps leading up to the incorrect invokation).

## Test Cases
We wrote unit tests for our project, contained in the `tests/` folder, to ensure the correctness of our access control mechanisms. We set these up and ran them using the third-party `pytest` library, but you can take a look at the tests for the various cases that we handle. For example, we generally test for:
- __Successful execution__ upon invokation with valid inputs.
- __Invalid inputs__ (eg. empty strings where these are not allowed).
- __Data integrity checks__, such as disallowing an attempt to overwrite the group an object is in, or disallowing an attempt to define multiple permissions with the same `(operation, usergroup)` keys.
- __Logical error cases__, such as a failure to authenticate because of an invalid password, or a denial of access if a user lacks permissions for an object.

## Implementation
The key piece of our implementation is the `AccessControlData` class within the `persistence.py` library. This class handles all operations for our scripts, and therefore stores all data in a single place accessible by all scripts. Whenever one of our scripts is run, we read in the `AccessControlData.pickle` file, and deserialize its contents into an `AccessControlData` instance. Once the invoked operation is completed, we serialize the contents of the `AccessControlData` instance and write it back to `AccessControlData.pickle`.

In particular, the `AccessControlData` class implements the following methods (which you will notice correspond directly with the various commands for our scripts):
- `add_user(username, password)`
- `authenticate(username, password)`
- `add_user_to_group(user, user_group)`
- `add_object_to_group(object_name, object_group)`
- `add_access(operation, usergroup, objgroup=None)`
- `can_access(operation, username, objname=None)`

### Data Structures
We organize the access control metadata using the following structures in `AccessControlData`:
- `users`: a hashmap with one-to-one mappings from usernames to their passwords:
  ```
  { 
    username1 : password1, 
    username2 : password2, 
    ... 
  }
  ```
- `users_to_groups`: a hashmap with one-to-many mappings from usernames to user groups (with keys being usernames and values being a `set` of the groups that user is in):
  ```
  { 
    username1: { group1, group2 }, 
    username2: { group2, group3 }, 
    ... 
  }
  ```
- `objects_to_groups`: a hashmap with one-to-one mappings from object names to object groups: 
  ```
  { 
    object1: object_group1, 
    object2: object_group3,
    object3: object_group1,
    object4: object_group2,
    ... 
  }
  ```
- `permissions`: a `set` of `(operation, usergroup, objectgroup)` tuples:
  ```
  {
    (read,  students, books),
    (drink, humans,   beverages),
    ...
  }
  ```
