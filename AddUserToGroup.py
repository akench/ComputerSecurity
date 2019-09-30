import sys

from persistence import AccessControlData

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Failure: Must specify only username and group name.")
        exit()
    _, username, group_name = sys.argv

    # load access control data from file
    access_control_data = AccessControlData.load_data()
    try:
        # add user to the group
        access_control_data.add_user_to_group(username, group_name)
        # write the updated data
        access_control_data.save_data()
    except Exception as e:
        print(e)
        exit()

    users_in_group = access_control_data.get_users_in_group(group_name)
    
    print("Success!")
    print(f"Users in group {group_name} = {users_in_group}")