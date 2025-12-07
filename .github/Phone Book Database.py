#This program was written by Logan Gibson on 12/6/25
#Its name is "Phone Book Database Interface"

#making the database requires sqlite
import sqlite3

#create the database
conn = sqlite3.connect('phonebook.db')

#add the cursor object
cur = conn.cursor()

#create the Entries table
cur.execute('''CREATE TABLE IF NOT EXISTS Entries(EntryID INTEGER PRIMARY KEY NOT NULL, 
            Name TEXT, PhoneNumber INTEGER)''')

#save changes
conn.commit

#end the connection
conn.close


#define global variables for menu navigation
MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

#create the main function that controls menu navigation
def main():
    
    choice = 0
    
    while choice != EXIT:
        
        display_menu()
        choice = get_menu_choice()
   
        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()

#show the menu's display
def display_menu():
    
    print('\n------- Phonebook Menu -------')
    print('1. Create a new entry')
    print('2. Read an entry')
    print('3. Update an entry')
    print('4. Delete an entry')
    print('5. Exit the phonebook')


#get the user's menu navigation choice
def get_menu_choice():
    choice = 0
    choice = int(input('Enter your choice:'))

    #make sure choice is valid
    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Valid choices are {MIN_CHOICE} through {MAX_CHOICE}.')
        choice = int(input('Enter your choice: '))

    return choice

#add a new entry to the Entries table
#note the insert_row() function
def create():
    print('Create New Entry')
    name = input('Person Name: ')
    phone_number = input('Phone Number: ')
    insert_row(name, phone_number)

#display an existing entry
#note the display_item() function
def read():
    name = input("Enter a person's name to search for: ")
    num_found = display_item(name)
    print(f'{num_found} row(s) found.')

#update an existing entry
#note the update_row() function
def update():
    
    #display existing entry so user can make an informed decision
    read()

    #change info
    selected_id = int(input('Select an entry ID: '))
    name = input("Enter the new person's name: ")
    phone_number = input('Enter the new phone number: ')
    num_updated = update_row(selected_id, name, phone_number)
    print(f'{num_updated} row(s) updated.')

#delete an existing entry
#note the delete_row() function
def delete():
    selected_id = int(input('Select an entry ID to delete: '))
    sure = input('Are you sure you want to delete this entry? (y/n): ')
    if sure.lower() == 'y':
        num_deleted = delete_row(selected_id)
        print(f'{num_deleted} row(s) deleted')

#logic to insert a new row in the Entries table
#this is referened by create()
def insert_row(name, phone_number):
    
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Entries
        (Name, PhoneNumber) VALUES (?, ?)''',
        (name, phone_number)) 
        conn.commit()

    except sqlite3.Error as err:
        print('Database Error', err)

    finally:
        if conn != None:
            conn.close()

#logic to display an existing entry
#this is referenced by read()
def display_item(name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute(''' SELECT * FROM Entries
                    WHERE lower(Name) == ?''',
                    (name.lower(),))
        results = cur.fetchall()
        for row in results:
            print(f'ID: {row[0]:<3}\n'
                  f'Name: {row[1]:<15}\n' 
                  f'Phone Number: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Database Error, err')
    finally:
        if conn != None:
            conn.close()

    return len(results)


#logic to update an existing entry
#this is referenced by update()
def update_row(id, name, phone_number):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Entries SET Name = ?, PhoneNumber = ?
                    WHERE EntryID == ?''',
                    (name, phone_number, id))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Database Error', err)
    
    finally:
        if conn != None:
            conn.close()

    return num_updated

#logic to delete a row
#this is referenced by delete()
def delete_row(id):
    conn = None
    num_deleted = 0
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Entries
                    WHERE EntryID == ?''', 
                    (id,))
        conn.commit()
        num_deleted = cur.rowcount

    except sqlite3.Error as err:
        print('Database Error', err)
    
    except ValueError as err:
        print('There was a problem finding someone with that name.' \
        'Make sure you spelled their name correctly.', err)

    finally:
        if conn != None:
            conn.close
    
    return num_deleted


#call the main function

if __name__ == '__main__':
    main()



