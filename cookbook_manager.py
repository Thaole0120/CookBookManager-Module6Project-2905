# Use the SQLite database
import sqlite3
from sqlite3 import Error

# Function to create a connection to the database
def create_connection():
    """Create a database connection"""
    conn = None
    try: 
        conn = sqlite3.connect('hipster_cookbooks.db');
        print(f"Succesflly connected to SQLite {sqlite3.version}  ")
        return conn
    except Error as e:
        print(f"Error establishing connection with the void: {e}")
        return None

# Function to create a table including tags, cookbook_tags and borrow_history
def create_table(conn):
    """Create a table structure including tags and cookbook_tags"""
    try: 
        # Create cookbooks table if it doesn't exist
        sql_create_cookbooks_table = """
        CREATE TABLE IF NOT EXISTS cookbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year_published INTEGER,
            aesthetic_rating INTEGER,
            instagram_worthy BOOLEAN,
            cover_color TEXT
        );"""
        
        # Create tags table if it doesn't exist
        sql_create_tags_table = """
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );"""
        
        # Create cookbook_tags table for many-to-many relationship
        sql_create_cookbook_tags_table = """
        CREATE TABLE IF NOT EXISTS cookbook_tags (
            cookbook_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            PRIMARY KEY (cookbook_id, tag_id)
        );"""
        
        # Create borrow_history table to track borrowed cookbooks
        sql_create_borrow_history_table = """
        CREATE TABLE IF NOT EXISTS borrow_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cookbook_id INTEGER,
            friend_name TEXT NOT NULL,
            date_borrowed TEXT NOT NULL,
            date_returned TEXT,
            FOREIGN KEY (cookbook_id) REFERENCES cookbooks (id)
        );"""
        
        # Calling the constructor for the cursor object to create a new cursor
        # that let us work with the database
        cursor = conn.cursor()
        cursor.execute(sql_create_cookbooks_table)
        cursor.execute(sql_create_tags_table)
        cursor.execute(sql_create_cookbook_tags_table)
        cursor.execute(sql_create_borrow_history_table)
        conn.commit()

        print("Successfully created a database structure for tags and borrowing history.")
    except Error as e:
        print(f"Error creating table: {e}")

# Function will insert a new cookbook record into the database 
def insert_cookbook(conn, cookbook):
    """Add a new cookbook to your shelf )"""
    sql = '''INSERT INTO cookbooks(title, author, year_published, aesthetic_rating,
            instagram_worthy, cover_color)
            VALUES(?,?,?,?,?,?)'''
    try:
        # Create a new cursor ( this is like a pointer that lets us traverse the database)
        cursor = conn.cursor()
        cursor.execute(sql, cookbook)
        # Commit the change
        conn.commit()
        print(f"Successfully curated cookbook with id: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding to collection: {e}")
        return None

# Function to retrieve the cookbooks from the database    
def get_all_cookbooks(conn):
    """Browse your entire collection """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cookbooks")
        # Put the resultset of cookbooks into a list called books
        books = cursor.fetchall()

        # Iterate through the list of books and display the info for each cookbook
        for book in books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]} (vintage is better)")
            print(f"Aesthetic Rating: {'✨' * book[4]}")
            print(f"Instagram Worthy: {'📸 Yes' if book[5] else 'Not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
        return books
    except Error as e:
        print(f"Error retrieving collection: {e}")
        return []

# Function to search cookbooks by aesthetic rating
def search_by_aesthetic_rating(conn, minimum_rating):
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # SQL query to search for cookbooks
        sql = """ SELECT id, title, author, year_published, aesthetic_rating, instagram_worthy, cover_color 
        FROM cookbooks
        WHERE aesthetic_rating >= ? AND instagram_worthy = 1
        ORDER BY cover_color ASC;
        """
        # Execute the query with the minimum_rating parameter
        cursor.execute(sql, (minimum_rating,))
        
        # Fetch all results
        photogenic_books = cursor.fetchall()
        
        # Display the results in a stylish way
        print("\nMost Photogenic Cookbooks (Perfect for Your Instagram Grid):")
        for book in photogenic_books:
            print(f"ID: {book[0]}")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Published: {book[3]}")
            print(f"Aesthetic Rating: {'✨' * book[4]}")
            print(f"Instagram Worthy: {'📸 Yes' if book[5] == 1 else 'Not aesthetic enough'}")
            print(f"Cover Color: {book[6]}")
            print("---")
        
        return photogenic_books
    except Error as e:
        print(f"Error searching for photogenic cookbooks: {e}")
        return []

# Function to add tags to a cookbook
def add_recipe_tags(conn, cookbook_id, tags):
    """
    Add tags to a cookbook (e.g., 'gluten-free', 'plant-based', 'artisanal')
    Creates new tags if they don't exist
    Links tags to the cookbook using the cookbook_tags table
    """
    try:
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Check if the cookbook exists in the database using its ID
        cursor.execute("SELECT * FROM cookbooks WHERE id = ?", (cookbook_id,))
        cookbook = cursor.fetchone()
        
        # If no cookbook is found with the given ID, display a message and exit the function
        if not cookbook:
            print(f"No cookbook found with ID: {cookbook_id}")
            return
        
        # Loop through each tag provided in the tags list
        for tag_name in tags:
            # Clean the tag by stripping whitespace and converting to lowercase
            tag_name = tag_name.strip().lower()
            
            # Skip empty tags (e.g., if the user accidentally entered a comma without text)
            if not tag_name:
                continue

            # Check if the tag already exists in the tags table
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag = cursor.fetchone()
            
            # If the tag does not exist, insert it into the tags table
            if not tag:
                cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
                conn.commit()  # Save changes to the database
                tag_id = cursor.lastrowid  # Get the ID of the newly inserted tag
                print(f"New tag added: {tag_name}")
            else:
                # If the tag already exists, get its ID
                tag_id = tag[0]
            
            # Check if the relationship between the cookbook and the tag already exists
            cursor.execute("""
                SELECT * FROM cookbook_tags 
                WHERE cookbook_id = ? AND tag_id = ?
            """, (cookbook_id, tag_id))
            existing_relationship = cursor.fetchone()
            
            # If the relationship does not exist, create it in the cookbook_tags table
            if not existing_relationship:
                cursor.execute("""
                    INSERT INTO cookbook_tags (cookbook_id, tag_id) 
                    VALUES (?, ?)
                """, (cookbook_id, tag_id))
                conn.commit()  # Save changes to the database
                print(f"Tag '{tag_name}' added to cookbook ID: {cookbook_id}")
            else:
                # If the relationship already exists, inform the user
                print(f"Tag '{tag_name}' is already associated with cookbook ID: {cookbook_id}")
                
    except Error as e:
        # Display an error message if any exception occurs during the process
        print(f"Error adding tags: {e}")

# Function to track borrowed cookbooks
def track_borrowed_cookbook(conn, cookbook_id, friend_name, date_borrowed):
    """
    Track which friend borrowed your cookbook and when
    Stores the borrowing record in the borrow_history table
    """
    try:
        # Create a cursor to interact with the database
        cursor = conn.cursor()
        
        # Check if the cookbook exists in the database using its ID
        cursor.execute("SELECT * FROM cookbooks WHERE id = ?", (cookbook_id,))
        cookbook = cursor.fetchone()
        
        # If no cookbook is found with the given ID, display a message and exit the function
        if not cookbook:
            print(f"No cookbook found with ID: {cookbook_id}")
            return
        
        # Prepare the SQL query to insert the borrowing record into the borrow_history table
        sql_insert_borrow = """
        INSERT INTO borrow_history (cookbook_id, friend_name, date_borrowed)
        VALUES (?, ?, ?);
        """
        
        # Execute the query with the provided cookbook ID, friend's name, and date borrowed
        cursor.execute(sql_insert_borrow, (cookbook_id, friend_name, date_borrowed))
        
        # Commit the changes to save the borrowing record in the database
        conn.commit()
        
        # Confirm the borrowing record has been saved successfully
        print(f"Cookbook ID {cookbook_id} borrowed by {friend_name} on {date_borrowed}")
        
    except Error as e:
        # Display an error message if any exception occurs during the process
        print(f"Error tracking borrowed cookbook: {e}")

# Main function is called when the program executes
# It directs the show
def main():
    # Establish connection to our artisanal database
    conn = create_connection()
    
    if conn is not None:
        # Create our free-range table
        create_table(conn)

            # Start the main application loop to keep the program running
            while True:
            # Display the main menu 
            print("\n--- Cookbook Collection Menu ---")
            print("1. View All Cookbooks")
            print("2. Add Tags to a Cookbook")
            print("3. Track Borrowed Cookbook")
            print("4. Exit")
            
            # Prompt the user to choose an option from the menu
            choice = input("Choose an option: ")
            

            if choice == '1':
                # Call the function to retrieve and display all cookbooks
                get_all_cookbooks(conn)
            elif choice == '2':
                # Prompt the user for the cookbook ID to tag
                cookbook_id = int(input("Enter the ID of the cookbook to tag: "))
                # Ask the user to enter tags separated by commas
                tags_input = input("Enter tags separated by commas: ")
                # Split the tags by comma and strip any extra whitespace
                tags = [tag.strip() for tag in tags_input.split(',')]
                # Call the function to add the tags to the specified cookbook
                add_recipe_tags(conn, cookbook_id, tags)
            elif choice == '3':
                cookbook_id = int(input("Enter the ID of the cookbook to track: "))
                friend_name = input("Enter your friend's name: ")
                # Record the date when the cookbook was borrowed
                date_borrowed = input("Enter the date borrowed (YYYY-MM-DD): ")
                # Call the function to track the borrowed cookbook in the database
                track_borrowed_cookbook(conn, cookbook_id, friend_name, date_borrowed)
            elif choice == '4':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        
    # After exiting the loop, close the database connection
    conn.close()

        conn.close()
    else:
        print("Error! Could not establish database connection.")

if __name__ == '__main__':
    main()

