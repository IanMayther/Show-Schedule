'''
Provides a basic frontend
'''
import sys
import logging
import main
import table_setup as ts


def load_users():
    '''
    Loads user accounts from a file
    '''
    pass


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    pass

def add_employee():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    user_add = main.add_user(user_id, email, user_name, user_last_name, user_collection)
    if not user_add:
        print("An error occurred while trying to add new user")
        return False

    print("User was successfully added")
    return True

def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
        return False

    print("User was successfully updated")
    return True

def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if  result:
        print(f"User ID: {user_id}")
        print(f"Email: {result[2]}")
        print(f"Name: {result[0]}")
        print(f"Last name: {result[1]}")
        return True

    print("ERROR: User does not exist")
    return False

def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
        return False

    print("User was successfully deleted")
    return True

def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
        return False

    print("New status was successfully added")
    return True

def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
        return False

    print("Status was successfully updated")
    return True

def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result:
        print(f"User ID: {result[1]}")
        print(f"Status ID: {result[0]}")
        print(f"Status text: {result[2]}")
        return True

    print("ERROR: Status does not exist")
    return False

def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
        return False

    print("Status was successfully deleted")
    return True

def search_all_status_updates():
    '''
    Searches all updates by user_id
    '''
    user_id = input('Enter User ID: ')
    stat_query = main.search_all_status_updates(user_id, status_collection)

    if len(stat_query) == 0:
        print('User_id: %s, Does Not Exist'%user_id)
        return False

    print('A total (%s) status updates found for %s'%(len(stat_query),user_id))
    gen = status_generator(stat_query)
    while True:
        see_update = input('Would you like to see the next update? (Y/N): ')
        if see_update.lower() == 'y':
            try:
                print(next(gen)[0])
            except StopIteration:
                print('List of found status concluded')
                break
        elif see_update.lower() == 'n':
            break
        else:
            print('Please select a valid input')

    return True

def status_generator(input_list):
    '''
    Generate status review
    '''
    for status_update in input_list:
        yield status_update

def filter_status_by_string():
    '''
    Filter all status be provided input
    '''

    sear_string = input('Enter search string: ')
    fnd_stat_it = main.filter_status_by_string(sear_string, status_collection)

    while True:
        rev_stat = input('Review next status? (Y/N): ')
        if rev_stat.lower() == 'y':
            try:
                next_result = next(fnd_stat_it)
                print(next_result.status_text)
                get_rid = input('Delete this status? (Y/N): ')
                if get_rid.lower() == 'y':
                    main.delete_status(next_result.status_id,
                        status_collection)

            except StopIteration:
                print('List of found status concluded')
                break
        elif rev_stat.lower() == 'n':
            break
        else:
            print('Please select a valid input')

def flagged_status_updates():
    '''
    Prints all status tuples for matching string
    '''

    sear_string = input('Enter search string: ')
    fnd_stat_it = main.filter_status_by_string(sear_string, status_collection)

    return [print((status.status_id,
            status.status_text)) for status in fnd_stat_it]


def quit_program():
    '''
    Quits program
    '''

    logging.info("--Program closed--")
    sys.exit(0)

if __name__ == '__main__':
    logging.info("--Program executed--")
    ts.db_create()
    DATABASE = 'Install_Calendar.db'
    EC = main.init_employee_database(DATABASE)
    IC = main.init_installer_database(DATABASE)
    JC = main.init_job_database(DATABASE)

    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': search_all_status_updates,
        'M': filter_status_by_string,
        'N': flagged_status_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            H: Add status
                            I: Update status
                            J: Search status by status
                            K: Delete status
                            L: Search status by user
                            M: Search all status updates matching a string
                            N: Flagged status
                            Q: Quit
                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")