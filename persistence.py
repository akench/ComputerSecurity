import pickle
from collections import defaultdict

PICKLE_FILE_NAME = 'AccessControlData.pickle'


class AccessControlData:
    def __init__(self):
        # Username -> Password
        self.users = dict()
        # Username -> group name
        self.user_to_groups = defaultdict(set)
        # Object name -> group name
        self.object_to_group = dict()
        # Set of tuples of the form (op_name, user_group, obj_group)
        self.permissions = set()

    @staticmethod
    def load_data():
        try:
            with open(PICKLE_FILE_NAME, 'rb') as f:
                return pickle.load(f)
        except:
            return AccessControlData()

    def save_data(self):
        with open(PICKLE_FILE_NAME, 'wb') as f:
            pickle.dump(self, f)

    def add_user_to_group(self, user, user_group):
        if not user or not user_group:
            raise ValueError("Failure: Username or group name cannot be empty")
        if user not in self.users:
            raise ValueError("Failure: User does not exist!")

        self.user_to_groups[user].add(user_group)

    def add_object_to_group(self, object_name, object_group):
        if not object_name or not object_group:
            raise ValueError("Object name or group name cannot be empty")
        # assuming each object is in only one group
        self.object_to_group[object_name] = object_group

    def add_user(self, username, password):
        if not username or not password:
            raise ValueError("Failure: Username and password must not be empty")
        if username in self.users:
            raise KeyError(f"Failure: User '{username}' already exists")

        self.users[username] = password

    def authenticate(self, username, password):
        if not username or not password:
            raise ValueError("Failure: Username and password must not be empty")
        if username not in self.users:
            raise KeyError(f"Failure: User '{username}' does not exist")

        return self.users[username] == password

    def add_access(self, operation, usergroup, objgroup=None):
        if not operation or not usergroup:
            raise ValueError("Operation and user group must not be empty")
        
        permission = (operation, usergroup, objgroup)
        if permission in self.permissions:
            raise ValueError(f"The permission '{permission}' already exists")

        self.permissions.add(permission)

    def can_access(self, operation, username, objname=None):
        if not operation or not username:
            raise ValueError("Operation or username must not be empty")
        if objname is not None and objname not in self.object_to_group:
            raise KeyError(f"Object '{objname}' does not exist")
        if username not in self.user_to_groups:
            raise KeyError(f"User '{username}' is not in any groups")

        objgroup = self.object_to_group[objname] if objname else None
        for usergroup in self.user_to_groups[username]:
            if (operation, usergroup, objgroup) in self.permissions:
                return True
        return False        
        
    def get_objects_in_group(self, target_group):
        return { object_name 
                 for object_name, group_name in self.object_to_group.items() 
                 if group_name == target_group }

    def get_users_in_group(self, target_group):
        return { user 
                 for user, groups in self.user_to_groups.items()
                 if target_group in groups }