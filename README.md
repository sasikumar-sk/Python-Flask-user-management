# Flask User Management System

This is a Flask-based web application for managing users with basic features such as **registration**, **login**, **role-based access**, **user editing**, and **deleting**. The system supports two types of roles:
- **Admin**: Can create, edit, delete users, and assign roles.
- **User**: Can only view their profile and update their details.

## Features

- **User Registration**: Allows users to create accounts with a username, password, and role (admin or user).
- **User Login**: Authenticated users can log in to access the system.
- **Role Management**: Admin users can assign roles (admin or user) to new and existing users.
- **User Management**: Admin users can update user details (like username and role) and delete users.
- **Password Security**: Passwords are stored securely using **Werkzeug's** password hashing.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite (Database)

### Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-directory>
2. Install required dependencies:
   
	```bash
	pip install -r requirements.txt

3. Run the Flask application:
   ```bash
	python app.py

4. Open your browser and go to http://127.0.0.1:5000/ to access the app.

File Structure
 	```bash

	graphql
 
	- app.py               # Flask application logic
	- templates/           # HTML templates for user interface
	  - home.html          # User Dashboard
	  - login.html         # Login page
	  - register.html      # Registration page
	  - edit_user.html     # Edit User page
	- static/              # Static assets (e.g., CSS, JS)
	  - css/                # Custom CSS (if applicable)
	  - js/                 # Custom JS (if applicable)
	- users.db             # SQLite database storing users' information


### Screenshots
Home Page (User Dashboard)
Shows a welcome message, user list, and buttons to manage users (if admin).

Login Page
Allows users to log in.

Register Page
Allows users to register with their username, password, and role.

Edit User Page
Allows an admin to edit user details.

### Example Workflow
Register a User:

**Go to the registration page.**

- Enter the username, password, and select the role.
- The user will be saved to the database and can log in.

**Login:**
- Log in with your username and password.
- Admin Operations (only available to users with the admin role):
- Admins can manage users (add, edit, or delete).
- Admins can change the role of users.

- Logout: Once logged in, users can log out.

### Database Schema
- users: Stores the user details.
- id: Integer, primary key
- username: Text, unique
- password: Text, hashed password
- role: Text, either "admin" or "user"

### Technology Stack
- Backend: Flask
- Database: SQLite
- Frontend: HTML, CSS (Bootstrap), Font Awesome icons
- Security: Password hashing using Werkzeug
