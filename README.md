# -movie_library
About:
-----------
This project is about MovieApp, where we can see movies through an API, add them to our lists, and see other people's publicly created lists and add them to our own lists. It has authentication for username and password, and there is a search bar where we can see different movies. And also, I am performing here crud operations like add, where we can add the playlists, delete, where we can click on the remove button to delete them, and view all other publicly created lists. There is a navbar and buttons that help us navigate. 

## Features
1. User authentication (Sign In/Sign Up)
2. Movie search using OMDB API
3. Create and manage movie lists
4. Public and private lists

## Running the project

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## Deployment

This project is deployed on pythonanywhere. Access it [here](https://bsreeni.pythonanywhere.com).

Commands to run code:
----------------------
1) creating your own virtual environment:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   pip install virtualenv
   virtualenv venv
   .\venv\Scripts\Activate
2)pip install django
3)pip install requests

   
