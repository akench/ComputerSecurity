import sys
from persistence import AccessControlData

if not 3 <= len(sys.argv) <= 4:
    print("Failure: Incorrect number of arguments")
    exit(1)

access_control = AccessControlData.load_data()

try:
    access_control.add_access(*sys.argv[1:])
    access_control.save_data()
    print("Success")
except Exception as exc:
    print(exc)