import datetime
import re
import sys
import os

from peewee import *

db = SqliteDatabase('worklog.db')

class Entry(Model):
    
    task_mins = IntegerField()
    task_date = DateField()
    task_notes = TextField()
    employee_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    
    class Meta:
        database = db

def clear():
    """ Clears the screen """
    
    os.system("clear")

def initialize():
    """ Create the database and the table if they don't exist """
    db.connect()
    db.create_tables([Entry], safe=True)

def main_menu():
    """ Main menu of the program asking user to either add new entry, search existing ones or quit the program """
    while True:
        clear()
        print("""
    MAIN MENU
    -------------------------------
    Would you like to:
    
    [N]: Add a new entry.
    [S]: Search existing entries. 
    [Q]: Quit and exit the program. 
        """)
        entry_choice = input("Please select an option from above menu: ").lower().strip()
        
        if entry_choice == 'q':
            clear()
            sys.exit()
        elif entry_choice == 'n':
            clear()
            add_new_entry()
        elif entry_choice == 's':
            clear()
            search_menu()
        else:
            input("""Invalid choice, please check the menu options.
                  Press enter to continue""")
            clear()
            main_menu()        
    

def add_new_entry():
    """ Adds a new entry to the program """
    
    employee_name = get_employee_name()
    task_date = get_task_date()
    task_name = get_task_name()
    task_mins = get_task_mins()
    task_notes = input("Please enter any notes you would like to go with the task, press enter if none: ").lower().strip()
    
    entry = {"employee_name": employee_name,
    "task_name": task_name,
    "task_date": task_date,
    "task_mins": task_mins,
    "task_notes": task_notes}
    print("""
Would you like to:
[S]: Save this entry.
[E]: Edit this entry.
[D]: Delete this entry and go to main menu.
        """)
    add_entry_choice = input("Please select an option from the above menu: ").lower().strip()
    if add_entry_choice == 's': 
        Entry.create(**entry)
    elif add_entry_choice == 'e':
        while True:
            print("""
What would you like to edit:
[E]: Employee Name.
[D]: Date.
[T]: Time spent.
[N]: Task Name.
[S]: Task Notes.
[X]: Done.
                """)
            edit_choice = input("Please select an option from the above menu: ").lower().strip()
            if edit_choice == 'e':
                employee_name = get_employee_name()
            elif edit_choice == 'd':
                task_date = get_task_date()
            elif edit_choice == 't':
                task_mins = get_task_mins()
            elif edit_choice == 'n':
                task_name = get_task_name()
            elif edit_choice == 's':
                task_notes = input("Please enter any notes you would like to go with the task, press enter if none: ").lower().strip()
            elif edit_choice == 'x':
                Entry.create(**entry)
                input("Entry added! Press enter to continue")
                break
    elif add_entry_choice == 'd':
        clear()
        return None
    
    entry = {"employee_name": employee_name,
    "task_name": task_name,
    "task_date": task_date,
    "task_mins": task_mins,
    "task_notes": task_notes}
    
    return entry

def get_employee_name():
    """ Gets the employee name """
    
    employee_name = input("Please enter the employee name: ").strip()
    if len(employee_name) == 0:
        input("Employee name cannot be empty! Press enter to continue..")
        return get_employee_name()
    return employee_name  

def get_task_date(message = ""):
    """ Gets the task date """

    task_date = input("Please enter the {} date for the task in mm/dd/yyyy format or type 't' for today's date: ".format(message))
    if task_date == 't': 
        task_date = datetime.date.today().strftime("%m/%d/%Y")
        return task_date
    try:
        datetime.datetime.strptime(task_date, "%m/%d/%Y")
    except ValueError:
        input("Not a valid date entry, please enter in mm/dd/yyyy format! Press enter to continue..")
        return get_task_date()
    else:
        return task_date


def get_task_name():
    """ Gets the task name """

    task_name = input("Please enter a task name: ").lower().strip()
    if len(task_name) == 0:
        input("Task name cannot be empty! Press enter to continue..")
        return get_task_name()
    return task_name

def get_task_mins():
    """ Gets the task mins """

    task_mins = input("Please enter the number of mins spent on the task: ")
    try:
        int(task_mins)
    except ValueError:
        input("Not a valid entry, task mins should be a integer! Press enter to coontinue..")
        return get_task_mins()
    else:
        return int(task_mins)

def search_menu():
    """ Searches existing entries either by date, time spent, exact string match or pattern/regex match """
    
    while True:
        print("""
    Would you like to search by:
    
    [M]: Go back to main menu.
    [N]: Search by employee name.
    [D]: Search by date.
    [T]: Search by time spent.
    [E]: Search by exact string match in task name and task notes.
    [Q]: Quit and exit the program.
        """)
        find_by_choice = input("Please select an option from the above search menu: ").lower().strip()
        
        if find_by_choice == 'q':
            clear()
            sys.exit()
        elif find_by_choice == 'n':
            clear()
            return search_by_employee_name()
        elif find_by_choice == 'd':
            clear()
            return search_by_date_menu()
        elif find_by_choice == 't':
            clear()
            return search_by_time_spent()
        elif find_by_choice == 'e':
            clear()
            return search_by_exact_match()
        elif find_by_choice == 'm':
            clear()
            main_menu()
        else:
            input("""Invalid choice, please check the menu options.
                  Press enter to continue""")
            clear()
            return search_menu()

def retrieve_all_entries():
    """ Retrieves all entries from database """
    return Entry.select().order_by(Entry.task_date.desc())

def search_by_date_menu():
    """ Search by date or date range """
    
    print(""" 
Would you like to:

[D]: Search by individual date.
[R]: Search by date range.
[Q]: Quit and exit the program.
    """)
    
    date_search_choice = input("Please select an option from the above date search menu: ").lower().strip()
    
    if date_search_choice == 'q':
        clear()
        sys.exit()
    elif date_search_choice == 'd':
        clear()
        search_results = search_by_date()
    elif date_search_choice == 'r':
        clear()
        search_results = search_by_date_range()
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        return search_by_date_menu()
    return search_results

def search_by_employee_name():
    """ Search by employee name """

    entries = retrieve_all_entries()
    search = get_employee_name()
    entries = entries.where(Entry.employee_name.contains(search))
    if entries.count() > 0:
        print_entries(entries)
        return entries
    else:
        input("No entries were found!!! Press enter to continue..")
        return None

def search_by_date():
    """ Search by date """

    entries = retrieve_all_entries()
    dates = []
    idx = 0
    for entry in entries:
        if entry.task_date in dates: continue
        idx += 1
        print("{}: {}".format(idx, entry.task_date))
        dates.append(entry.task_date)
    date_index = input("Choose the index of the date from the above list to lookup entries on that date: ")
    print("")
    entries = entries.where(Entry.task_date == dates[int(date_index) - 1])
    print_entries(entries)
    return entries

        
def search_by_date_range():
    """ Search by date range """

    entries = retrieve_all_entries()
    dates = []
    idx = 0
    for entry in entries:
        if entry.task_date in dates: continue
        idx += 1
        print("{}: {}".format(idx, entry.task_date))
        dates.append(entry.task_date)
    #date_range = input("Provide a range of dates from the above list, in mm/dd/yyyy format (e.g. 12/01/2016,12/08/2016) to lookup entries between those dates: ")
    start_date = get_task_date("start")
    end_date = get_task_date("end")
    print("")
    entries = entries.where((Entry.task_date >= start_date) & (Entry.task_date <= end_date))
    if entries.count() > 0:
        print_entries(entries)
        return entries
    else:
        input("No entries were found!!! Press enter to continue..")
        return None
                

def del_or_update_entry_menu(entry, paging = False):
    """ Menu for deleting or updating entries from a given list """

    if paging == False: print("""
Would you like to:

[N]: Do nothing and return.
[U]: Update the above entry.
[D]: Delete the above entry.
[Q]: Quit and exit the program.
""")
    else: print("""
Would you like to:

[M]: Return to the main menu.
[U]: Update the above entry.
[D]: Delete the above entry.
[Q]: Quit and exit the program.
[C]: Continue paging.
""")

    del_update_choice = input("Please select an option from the above menu: ").lower().strip()
    
    if del_update_choice == 'q':
        clear()
        sys.exit()
    elif del_update_choice == 'm':
        clear()
        main_menu()
    elif del_update_choice == 'u':
        return update_entry(entry)
    elif del_update_choice == 'd':
        return delete_entry(entry)
    elif del_update_choice == 'c' and paging == True:
        return 1
    else:
        input("""Invalid choice, please check the menu options.
              Press enter to continue""")
        return del_or_update_entry_menu(entry)

        
def update_entry(entry):
    """ Updates an entry """

    #update_entry_idx = input("Which entry would you like to update, please select the index for that entry (e.g.,1): ")
    print("""
What would you like to update:
[E]: Employee Name
[D]: Date
[T]: Time spent
[N]: Task Name
[S]: Task Notes
        
        """)
    #if len(entries_to_update_from) == 1: update_entry_idx = 1
    update_choice = input("Please select an option from the above menu: ").lower().strip()
    if update_choice == 'e':
        new_name = get_employee_name()
        entry.employee_name = new_name
        entry.save()
    elif update_choice == 'd':
        new_date = get_task_date()
        entry.task_date = new_date
        entry.save()
    elif update_choice == 'n':
        new_task_name = get_task_name()
        entry.task_name = new_task_name
        entry.save()
    elif update_choice == 't':
        new_time_spent = get_task_mins()
        entry.task_mins = new_time_spent
        entry.save()                           
    elif update_choice == 's':
        new_notes = input("Please enter new notes: ")
        entry.task_notes = new_notes
        entry.save()
    input(""" Entry/Entries updated! Press enter to continue """)
    clear()
    return entry
        
def delete_entry(entry):
    """ Deletes an entry """

    if input("Are you sure you want to delete this entry? [Y]: Yes, [N]: No").lower().strip() == "y":
        entry.delete_instance()
        input("""Entry/Entries deleted! Press enter to continue """)
    clear()
    return None
     

def search_by_time_spent():
    """ Search the worklog entries by time spent """

    entries = retrieve_all_entries()
    search = get_task_mins()
    entries = entries.where(Entry.task_mins == search)
    if entries.count() > 0:
        print_entries(entries)
        return entries
    else:
        input("No entries were found!!! Press enter to continue..")
        return None

                
def search_by_exact_match():
    """ Search the worklog entries by exact string match in task name or task notes """

    entries = retrieve_all_entries()
    search = input("Please provide the exact string you would like to search for in task names or task notes: ")
    entries = entries.where(Entry.task_name.contains(search) | Entry.task_notes.contains(search)) 
    if entries.count() > 0:
        print_entries(entries)
        return entries
    else:
        input("No entries were found!!! Press enter to continue..")
        return None

def print_entries(entries_to_print):
    """ Gives an option to the user to either look all the entries at the same time or page through them """

    print("""
Would you like to:

[A]: Display all the entries at the same time.
[P]: Page through the entries one at a time.
        """)
    print_choice = input("Please select an option from the above menu: ").lower().strip()
    if print_choice == 'a':
        for i, entry in enumerate(entries_to_print):
            print("\n{}: Employee name: {}\n   Task name: {}\n   Task date: {}\n   Task time spent: {}\n   Task notes: {}\n".format(i + 1, entry.employee_name, entry.task_name, entry.task_date, entry.task_mins, entry.task_notes))
        input("Press enter to continue")
    elif print_choice == 'p':
        display_entries(entries_to_print)
        #main_menu()


def display_paging_options(index, entries):
    """ Displays a menu that let's the user page through the entries."""

    print("\n")
    p = "[P] - Previous entry"
    n = "[N] - Next entry"
    q = "[Q] - Quit and return to Main Menu"
    menu = [p, n, q]

    if index == 0:
        menu.remove(p)
    elif index == len(entries) - 1:
        menu.remove(n)

    for option in menu:
        print(option)


def display_entries(entries):
    """ Pages the entries to the screen."""
    index = 0

    while True:
        clear()
        print("\n{}: Employee name: {}\n   Task name: {}\n   Task date: {}\n   Task time spent: {}\n   Task notes: {}\n".format(index + 1, entries[index].employee_name, entries[index].task_name, entries[index].task_date, entries[index].task_mins, entries[index].task_notes))
        del_or_update_entry_menu(entries[index], paging = True)

        if len(entries) == 1:
            input("Press ENTER to continue to the main menu.")
            return

        display_paging_options(index, entries)

        page_choice = input("Please select an option from the above menu: ").lower().strip()

        if index == 0 and page_choice == 'n':
            index += 1
            clear()
        elif index > 0 and index < len(entries) - 1 and page_choice == 'n':
            index += 1
            clear()
        elif index > 0 and index < len(entries) - 1 and page_choice == 'p':
            index -= 1
            clear()
        elif index == len(entries) - 1 and page_choice == 'p':
            index -= 1
            clear()
        elif page_choice == 'q':
            return
        else:
            input("""Invalid choice, please check the menu options.
              Press enter to continue""")

if __name__ == '__main__':
    clear()
    initialize()
    main_menu()

