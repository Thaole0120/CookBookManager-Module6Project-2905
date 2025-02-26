# CookBookManager-Module6Project-2905
This is the cookbook manager app for the ITEC2905 Module 6 Project

## Features Implemented  
1. View All Cookbooks  
   - Displays all cookbooks currently in your database, including their title, author, year published, aesthetic rating, Instagram worthiness, and cover color.  

2. Recipe Tagging System 
   - Add tags to cookbooks (e.g., "gluten-free", "vegan", "artisanal").  
   - Tags are stored uniquely and linked to multiple cookbooks using many-to-many relationship
   - Avoids duplicate tags by checking if a tag already exists before adding it.  

3. Cookbook Borrowing Tracker  
   - Track which friend borrowed your cookbook and when.  
   - Records the date borrowed and (optionally) the return date.  
   - Helps you keep track of who has your cookbooks and prevents losing them. 

## Additional Features  
- Consistent Display Format
  - Stylish and consistent output for all cookbook details.  
- Error Handling and Input Validation:
  - Checks for invalid inputs, such as non-numeric IDs or empty tag names.  
  - Displays meaningful error messages for database issues.  
- Many-to-Many Relationship for Tags:  
  - Cookbooks can have multiple tags, and the same tag can be linked to multiple cookbooks. 

## How to run your code
- Run the command: python cookbook_manager.py
- Then you will see a menu like this: 
--- Cookbook Collection Menu ---
View All Cookbooks
Add Tags to a Cookbook
Track Borrowed Cookbook
Exit Choose an option:

## Known limitations or issues
- No Deletion Option:  
    - Currently, there is no option to delete cookbooks, tags, or borrowing records.  
- Input Validation:
    - Although basic input validation is implemented, further checks could be added for date formats and special characters.  


