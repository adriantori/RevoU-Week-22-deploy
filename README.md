# Project README - Week 22 Assignment

## Overview:

This project implements a Flask-based backend for a ToDo application with user authentication and authorization. Users can register, log in, create, retrieve, update, and delete ToDo items. The application also distinguishes between user roles (USER and ADMIN) to control access to certain functionalities.

## Features:

- **User Authentication:**
  
  - Register: Users can register by providing a username, password, and optional role (default is USER).
  - Login: Registered users can log in to obtain an access token.

- **ToDo Management:**
  
  - Create ToDo: Authenticated users can create ToDo items by providing task details.
  - Retrieve ToDo: Users can retrieve their own ToDo items or, if an ADMIN, retrieve all ToDo items.
  - Update ToDo: Users can update their own ToDo items.
  - Delete ToDo: Users can mark their own ToDo items as deleted.

## How to Use:

1. **Clone the Project:**
   
   ```bash
   git clone https://github.com/your-username/your-todo-project.git
   cd your-todo-project
   ```

2. **Set Up Virtual Environment:**
   
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. **Initialize Database:**
   Uncomment the following lines in `app.py` to initialize the database (if needed):
   
   ```python
   # with app.app_context():
   #     db_init()
   ```

4. **Run the Application:**
   
   ```bash
   flask run
   ```

5. **Import Postman Collection:**
   Import the provided Postman collection data located in the root folder.

6. **Access Endpoints:**
   
   - Use Postman to interact with the following endpoints:
     - `/register` (POST): Register a new user.
     - `/login` (POST): Obtain an access token by logging in.
     - `/create` (POST): Create a new ToDo item.
     - `/get` (GET): Retrieve ToDo items based on user role.
     - `/update/<int:todo_id>` (PUT): Update a ToDo item.
     - `/delete/<int:todo_id>` (DELETE): Delete a ToDo item.

7. **API Usage Flow:**
   
   - Register a new user.
   - Log in to obtain an access token.
   - Use the access token to interact with ToDo endpoints.

## Models:

### User:

```python
from db import db
from enum import Enum
from sqlalchemy import Enum as EnumType
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserRole(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(EnumType(UserRole), default=UserRole.USER, nullable=False)
```

### ToDo:

```python
from db import db
from enum import Enum
from sqlalchemy import Enum as EnumType
from datetime import datetime

class ToDoPriority(Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    priority = db.Column(EnumType(ToDoPriority), default=ToDoPriority.LOW, nullable=False)
    due = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
```

## Important Code Snippets:

### Registration:

```python
existing_user = User.query.filter_by(username=username).first()
if existing_user:
    return {'error_message': 'Username already in use'}, 400

hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
new_user = User(username=username, password=hashed_password, role=UserRole[role])
db.session.add(new_user)
db.session.commit()
```

### Login:

```python
user = User.query.filter_by(username=username).first()

if user and bcrypt.check_password_hash(user.password, password):
    access_token = create_access_token(identity=user.id)
    return {'token': access_token}, 200
else:
    return {'error_message': 'Invalid username or password'}, 401
```

### Get ToDo:

```python
user = User.query.filter_by(id=user_id).first()

if not user:
    return {'error_message': 'User not found'}, 404

if user.role == UserRole.USER:
    todos = ToDo.query.filter_by(user_id=user_id, is_deleted=False).all()
elif user.role == UserRole.ADMIN:
    todos = ToDo.query.all()
else:
    return {'error_message': 'Invalid role'}, 400
```

### Update ToDo:

```python
todo = ToDo.query.filter_by(id=todo_id).first()

if not todo:
    return {'error_message': 'ToDo not found'}, 404

if todo.user_id != user_id:
    return {'error_message': 'Unauthorized to update this ToDo'}, 403

todo.task = updated_task
todo.priority = updated_priority
todo.due = updated_due
db.session.commit()
```

### Delete ToDo:

```python
todo = ToDo.query.filter_by(id=todo_id).first()

if not todo:
    return {'error_message': 'ToDo not found'}, 404

if todo.user_id != user_id:
    return {'error_message': 'Unauthorized to delete this ToDo'}, 403

if todo.is_deleted:
    return {'error_message': 'ToDo already deleted'}, 400

todo.is_deleted = True
db.session.commit()
```

## Front-End Explanations

I used [Material UI](https://mui.com) for my UI Library. why? because I want it.

Honesty, there's not much to explain here for now, because I used very simple site similar to Week 13 project, with addition of DatePicker from MUI for Due Date.

As for security, I got A on [Security Header](https://securityheaders.com), but I'm not gonna screenshot it here because im WAY too lazy. Just trust me on this, bro.
