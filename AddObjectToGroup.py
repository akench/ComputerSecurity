import sys

from persistence import AccessControlData

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError("Must specify only object name and group name.")
    _, object_name, group_name = sys.argv

    # load access control data from file
    access_control_data = AccessControlData.load_data()
    try:
        # add user to the group
        access_control_data.add_object_to_group(object_name, group_name)
        # write the updated data
        access_control_data.save_data()
    except Exception as e:
        print(e)
        exit()

    # get all objects in the group that was inserted
    objects_in_group = access_control_data.get_objects_in_group(group_name)

    print("Success!")
    print(f"Objects in group {group_name} = {objects_in_group}")
