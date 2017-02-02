import unittest
import unittest.mock
from playhouse.test_utils import test_database

import worklog
from peewee import *

test_db = SqliteDatabase(':memory:')
test_db.connect()
test_db.create_tables([worklog.Entry], safe=True)

TEST = {"employee_name": "Bill",
         "task_name": "test",
         "task_date": "01/01/2017",
         "task_mins": 200,
         "task_notes": "test notes"
         }

TEST1= {"employee_name": "Jack",
         "task_name": "project",
         "task_date": "01/05/2017",
         "task_mins": 100,
         "task_notes": "test notes"
         }

class DatabaseTest(unittest.TestCase):

    @staticmethod
    def create_entries():
        worklog.Entry.create(
            employee_name=TEST["employee_name"],
            task_name=TEST["task_name"],
            task_date=TEST["task_date"],
            task_mins=TEST["task_mins"],
            task_notes=TEST["task_notes"])

        worklog.Entry.create(
            employee_name=TEST1["employee_name"],
            task_name=TEST1["task_name"],
            task_date=TEST1["task_date"],
            task_mins=TEST1["task_mins"],
            task_notes=TEST1["task_notes"])
        
    def test_get_employee_name(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "alex"]):
            assert worklog.get_employee_name() == "alex"

    def test_get_task_mins(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", 10]):
            assert worklog.get_task_mins() == 10

    def test_get_task_name(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "proj"]):
            assert worklog.get_task_name() == "proj"            

    def test_get_task_date(self):
        with unittest.mock.patch('builtins.input', side_effect = ["", "", "01/01/2017"]):
            assert worklog.get_task_date() == "01/01/2017"   
            
    def test_add_new_enty(self):
        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "s"]):
            assert worklog.add_new_entry()["task_date"] == TEST["task_date"]  

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "e", "d", "01/05/2017", "x", ""]):
            assert worklog.add_new_entry()["task_date"] == "01/05/2017" 

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "e", "t", 15, "x", ""]):
            assert worklog.add_new_entry()["task_mins"] == 15 

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "e", "n", "project5", "x", ""]):
            assert worklog.add_new_entry()["task_name"] == "project5" 

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "e", "e", "John", "x", ""]):
            assert worklog.add_new_entry()["employee_name"] == "John" 

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "e", "s", "new_notes", "x", ""]):
            assert worklog.add_new_entry()["task_notes"] == "new_notes" 

        with unittest.mock.patch('builtins.input', side_effect = ["Bill", "01/01/2017", "test", 200, "notes", "d"]):
            assert worklog.add_new_entry()== None

    def test_search_by_date(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["j", "", "d", "j", "", "d", "1", "a", ""]):
                assert worklog.search_menu().count()  == 1

    def test_search_by_date_range(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["r", "01/01/2017", "01/10/2017", "a", ""]):
                assert worklog.search_by_date_menu().count()  == 2

            with unittest.mock.patch('builtins.input', side_effect = ["r", "04/01/2017", "04/10/2017", "a", ""]):
                assert worklog.search_by_date_menu()  == None

    def test_search_by_employee_name(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["n", "Bill", "a", ""]):
                assert worklog.search_menu().count()  == 1

            with unittest.mock.patch('builtins.input', side_effect = ["n", "Billy", "a", ""]):
                assert worklog.search_menu() == None

    def test_search_by_time_spent(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["t", "200", "a", ""]):
                assert worklog.search_menu().count()  == 1

            with unittest.mock.patch('builtins.input', side_effect = ["t", "2", "a", ""]):
                assert worklog.search_menu() == None

    def test_search_by_exact_match(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["e", "notes", "a", ""]):
                assert worklog.search_menu().count()  == 2

            with unittest.mock.patch('builtins.input', side_effect = ["e", "new_note", "a", ""]):
                assert worklog.search_menu() == None

    def test_search_by_exact_match2(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            with unittest.mock.patch('builtins.input', side_effect = ["test", "p", "c", "n", "c", "p", "c", "q"]):
                assert worklog.search_by_exact_match().count()  == 2

    def test_retrieve_all_entries(self):
        with test_database(test_db, (worklog.Entry, )):
            self.create_entries()
            assert worklog.retrieve_all_entries().count()  == 2

    def test_update_entry(self):
        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["j", "", "u", "e", "Jason", ""]):
                worklog.del_or_update_entry_menu(entry)
                self.assertEqual(entry.employee_name, "Jason")

        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["u", "n", "task2", ""]):
                worklog.del_or_update_entry_menu(entry)
                self.assertEqual(entry.task_name, "task2")

        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["u", "t", "11", ""]):
                worklog.del_or_update_entry_menu(entry)
                self.assertEqual(entry.task_mins, 11)

        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["u", "s", "new notes", ""]):
                worklog.del_or_update_entry_menu(entry)
                self.assertEqual(entry.task_notes, "new notes")

        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["u", "d", "01/02/2016", ""]):
                worklog.del_or_update_entry_menu(entry)
                self.assertEqual(entry.task_date, "01/02/2016")

    def test_delete_entry(self):
        with test_database(test_db, (worklog.Entry, )):
            entry = worklog.Entry.create(**TEST)
            with unittest.mock.patch('builtins.input', side_effect = ["d", "y", ""]):
                assert worklog.del_or_update_entry_menu(entry) == None


if __name__ == "__main__":
    unittest.main()

