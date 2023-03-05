"""
This is the capstone database project to create an ebookstore system. Bookstore clerks can add, change, delete and
search books via the system.

From working with this project, the following is learnt and considered.

- When using fetchall(), it returns "0" when the result set is empty but fetchone() returns
"None". Therefore, it has to be careful in writing code for these two functions.

- When designing the search options, normal situations is considered. For example, an option for user to list out all
the books in the system when he/she has no idea what is in the system. For experience staff, they can use book id, title
or author as searching criteria to quickly located the book they want.

- As the "id" field in the books table is defined as INTEGER PRIMARY KEY (rowid), its value will be auto-incremented and
generated when a new record is added. Therefore, users only need to provide the value for the title, author and quantity
field when adding new books.

- Users are offered a chance to double confirm before making change to the database.

- Define validation and checking on users' input throughout the program to handle predictable errors.

START
1. Create a database "ebookstore"
2. Create a table "books"
3. Load data into the table. This only happens when the table has no record.
4. Create a user menu for bookstore clerk to add, update, delete and search books
5. Define specific functions for add, update, delete and search books.
END
"""

import sqlite3
from tabulate import tabulate

# Define global variables and dictionaries that are required for the main and function modules
headers = ["ID", "TITLE", "AUTHOR", "QTY"]
key_matching = {
    "id": "id",
    "ti": "title",
    "au": "author"
}


def init_db():
    # Create table 'books' if it doesn't exist.
    cursor.execute('''create table if not exists books(id INTEGER PRIMARY KEY,
        title varchar(50) not null, author varchar(30) not null, qty int not null)''')
    db.commit()

    books_data = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                  (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
                  (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                  (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                  (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

    # Load the data into the table if it is empty.
    numb_record = cursor.execute('''select * from books''').fetchall()
    if len(numb_record) == 0:
        cursor.executemany('''insert into books(id, title, author, qty) values(?,?,?,?)''', books_data)
        db.commit()


# This function is to search the information from the database based on different criteria like book id, book titles or
# book authors entered by users. Implementing the code as function reduces duplicated coding and chances of errors.
def search_db(sch_opt, sch_value):

    sch_field = key_matching[sch_opt]
    # Convert integer data type to string before passing to "SELECT FROM TABLE WHERE LIKE %" statement
    if isinstance(sch_value, int):
        sch_value = str(sch_value)

    cursor.execute('''select * from books where %s like ?''' % sch_field, ('%' + sch_value + '%',))
    search_result = cursor.fetchall()
    if len(search_result) > 0:
        print(tabulate(search_result, headers, tablefmt='grid'))
    else:
        print(f"\nNo matched for book {sch_field}")


def add_book():

    book_title = input("New book title: ")
    if book_title == "":
        print("\nBook title was not entered")
        return

    book_author = input("New book author: ")
    if book_author == "":
        print("\nBook author was not entered")
        return

    try:
        book_qty = int(input("New book qty: "))
    except ValueError:
        print("\nBook quantity was not valid")
        return

    # Let users confirm the information before the record is inserted.
    confirm = input(f"""
New book information
====================
[Title]:\t{book_title}
[Author]:\t{book_author}
[Qty]:\t\t{book_qty}
Confirm to proceed (Y/N): """).lower()
    if confirm == 'y':
        cursor.execute('''insert into books(title, author, qty) values(?,?,?)''', (book_title, book_author, book_qty))
        db.commit()
        print("\nThe book is added")


def upt_book():

    try:
        # Design to let users change their mind and leave the function.
        chg_id = int(input("\nPlease enter the book id to update or 0 to return to main menu: "))
        if chg_id == 0:
            return
    except ValueError:
        # if the book id is invalid, it prints a warning message and leaves the function.
        print("\nInvalid book id")
        return

    # Retrieve the corresponding record for further process.
    cursor.execute('''select * from books where id = ?''', (chg_id,))
    result = cursor.fetchone()

    # Only proceed if the record exists. Otherwise, leave this function.
    if result is not None:

        # Loop through all the fields for users to decide what fields need to be updated.
        new_title = input(f"Current book name: [{result[1]}]. Enter a new name or press enter to move on: ")
        if new_title == "":
            new_title = result[1]

        new_author = input(f"Current book author: [{result[2]}]. Enter a new author or press enter to move on: ")
        if new_author == "":
            new_author = result[2]

        new_qty = input(f"Current book quantity [{result[3]}]. Enter a new quantity or press enter to move on: ")
        if new_qty == "":
            new_qty = result[3]
        else:
            try:
                new_qty = int(new_qty)
            except ValueError:
                print("\nInvalid book quantity")
                return
            if new_qty < 0:
                print("\nBook Quantity Can't Be Less Than 0")
                return

        # Let users confirm the information before the record is inserted.
        confirm = input(f"""
Updated book information
========================
[Id]:\t\t{chg_id}
[Title]:\t{new_title}
[Author]:\t{new_author}
[Qty]:\t\t{new_qty}
Confirm to proceed (Y/N): """).lower()
        if confirm == 'y':
            cursor.execute('''update books set title = ?, author = ?, qty = ? where id = ?''', (new_title, new_author,
                                                                                                new_qty, chg_id,))
            db.commit()
            print("\nThe book is updated")
    else:
        print("\nNo Matched Book Id")


def del_book():

    # As the book id is unique, it is the best to represent the book to be deleted.
    try:
        del_id = int(input("\nPlease enter the id of the book for delete: "))
    except ValueError:
        print("\nInvalid input for book id")
        return

    # Verify if the book id exists
    cursor.execute('''select * from books where id = ?''', (del_id,))
    result = cursor.fetchone()
    if result is not None:
        confirm = input(f"""
Book to be deleted
==================
[Id]:\t\t{result[0]}
[Title]:\t{result[1]}
[Author]:\t{result[2]}
Confirm to proceed (Y/N): """).lower()
        if confirm == 'y':
            cursor.execute('''delete from books where id = ?''', (del_id,))
            db.commit()
            print(f"\nThe book is deleted")
    else:
        print("\nInvalid book id")


def find_book():

    # The following search options are based on normal situations. In case users have no idea, they can simply
    # list out all the books to get some idea. Otherwise, book id, title or author are good searching criteria.
    # Like and % retrieve result set similar to the searching keywords.
    search_opt = input("""
Please select an option to search:
al - list all the books
id - search using book id
ti - search using book title
au - search using book author
ba - back to main menu
: """).lower()

    if search_opt == 'al':
        search_result = cursor.execute('''select * from books''').fetchall()
        if len(search_result) > 0:
            print(tabulate(search_result, headers, tablefmt='grid'))
        else:
            print("\nNo record found")

    elif search_opt == 'id':
        try:
            search_key = int(input("\nPlease enter the book id: "))
        except ValueError:
            print("\nInvalid book id")
            return
        search_db(search_opt, search_key)

    elif search_opt == 'ti':
        search_key = input("\nPlease enter the book title: ")
        if search_key == "":
            print("\nBook title was not entered")
        else:
            search_db(search_opt, search_key)

    elif search_opt == 'au':
        search_key = input("\nPlease enter the book author: ")
        if search_key == "":
            print("\nBook author was not entered")
        else:
            search_db(search_opt, search_key)

    elif search_opt == 'ba':
        print("\nYou now back to the main menu")

    else:
        print("\nInvalid option")


# ----- main program -----
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

# Create the books table and load data if necessary
init_db()

menu = """\nWelcome to the bookstore system! 

1 - Enter book
2 - Update book
3 - Delete book
4 - Search books
0 - Exit

Please choose an option: """

while True:

    try:

        choice = int(input(menu))

        if choice == 1:
            add_book()

        elif choice == 2:
            upt_book()

        elif choice == 3:
            del_book()

        elif choice == 4:
            find_book()

        elif choice == 0:
            db.close()
            print("\nGoodbye and have a nice day")
            break

        else:
            print("\nInvalid choice")

    except ValueError:
        print("\nInvalid choice")
