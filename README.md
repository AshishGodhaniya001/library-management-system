# library-management-system
# 📚 Library Management System

A web-based Library Management System built using **Python Django** and **MySQL**, allowing users to add, update, delete, search, and manage books with details like title, author, category, ISBN, and cover image. Includes a clean UI, role-based access, and live deployment on PythonAnywhere.

 **Live Demo:** https://ashu12.pythonanywhere.com/  
 **Tech Stack:** Django, Python, MySQL, HTML, CSS, Bootstrap

---

##  Features

-  **User Authentication**
  - Student / Normal User registration and login
  - Librarian / Admin login for management

-  **Book Management**
  - Add, edit, delete books
  - Store title, author, category, ISBN, description, and cover image
  - All books listed in a clean table / card layout

-  **Search & Filter**
  - Search books by name / title
  - Filter using keywords and ISBN

-  **Issue Request System**
  - Students can request a book to issue
  - Librarian can view all requests and approve / reject them
  - Students can see the status of their requests

-  **Dashboards**
  - **Student dashboard:** view available books, my issue requests, status, etc.
  - **Librarian dashboard:** manage books, manage issue requests, track issued books.

-  **Deployed Online**
  - Live on **PythonAnywhere** so anyone can access and test the system from browser.

---

##  How to Use (Live Website)

### As a Student / User

1. Open the website: **https://ashu12.pythonanywhere.com/**
2. Register a new account (if registration is enabled) or log in with existing credentials.
3. Browse the list of books from the home page.
4. Use the **search bar** to find books by name or ISBN.
5. Open a book detail page to see more information.
6. Click on **Request Issue** (if available) to request that book.
7. Go to **"My Issues" / "My Requests"** page to see:
   - Which books you have requested
   - Whether your request is **Pending / Approved / Rejected**.

### As a Librarian / Admin

1. Go to Django admin: `https://ashu12.pythonanywhere.com/admin/`
2. Log in using admin username & password.
3. From the admin panel you can:
   - Add / edit / delete books
   - Manage users
   - See book transactions / requests
4. From the librarian dashboard page (inside the app) you can:
   - View all **issue requests**
   - Approve / reject student requests
   - Track which books are currently issued.

---

##  How to Run Locally (Developer Setup)


1. **Clone the repository**
   git clone https://github.com/AshishGodhaniya001/library-management-system.git
   cd library-management-system https://github.com/AshishGodhaniya001/library-management-system.git
   cd library-management-system

2. **Create and activate virtual environment**
   python -m venv venv
   venv\Scripts\activate   # Windows

3.**Install required packages**
  pip install django
  # plus mysqlclient or other packages as per your setup

4.**Apply migrations**
  python manage.py migrate

5.**Create superuser**
  python manage.py createsuperuser

6.**Run the development server**
  python manage.py runserver

7.**Open http://127.0.0.1:8000/ in your browser to use the app locally. **
