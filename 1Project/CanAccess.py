import sys
from persistence import AccessControlData

if not 3 <= len(sys.argv) <= 4:
    print("Failure: Incorrect number of arguments")
    exit(1)

access_control = AccessControlData.load_data()

try:
    if access_control.can_access(*sys.argv[1:]):
        print("Success, user has permission to perform operation")
    else:
        print("Failure: User is not authorized to perform operation")
except Exception as e:
    print(e)