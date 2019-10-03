import sys
from persistence import AccessControlData

if len(sys.argv) != 3:
    print("Failure: Incorrect number of arguments")
    exit(1)

_, username, password = sys.argv
access_control = AccessControlData.load_data()

try:
    access_control.add_user(username, password)
    access_control.save_data()
    print("Successfully added user")
except Exception as exc:
    print(exc)
