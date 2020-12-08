
Comment System
============
## How to Run

### Prequisites
- [Python](https://www.python.org/downloads/)

From inside the repository root:

- Install packages  
````
  pip install -r requirements.txt
````
- Run database migrations
````
  python manage.py makemigrations
  python manage.py migrate
````
- Start the application
````
  python manage.py runserver
````

Then open http://127.0.0.1:8000/ in your browser

## Requirements
- Add Comments
- View Comments
- Reply to Comments (Infinite nesting)
- Search Comments by text
- Comments can have text and images

## Tech Stack Used

- Django
- SQLite

## Database Schema

![Database Schema](https://i.imgur.com/Dna4ySw.png)

### Notes :
- Each Reply Comment references its parent comment (the one it is a reply to)
- Root Comments have parent_comment = null
- Each Comment has a depth with root comments having depth = 0
