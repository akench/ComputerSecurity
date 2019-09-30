import sys
from persistence import AccessControlData

if len(sys.argv) != 3:
    print("Failure: Incorrect number of arguments")
    exit(1)

_, username, password = sys.argv
access_control = AccessControlData.load_data()

try:
    if access_control.authenticate(username, password):
        print("Success")
    else:
        print("Failure: Invalid password")
except Exception as exc:
    print(exc)
