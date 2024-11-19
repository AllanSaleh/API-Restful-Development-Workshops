# ORM (Object-Relational Mapper)

An **ORM (Object-Relational Mapper)** is a tool that helps you work with databases using Python objects instead of writing raw SQL queries. It makes interacting with the database easier and more intuitive by treating database rows like Python objects.

**SQLAlchemy** is a popular Python library that provides ORM capabilities. With SQLAlchemy, you can:

- Define your database tables as Python classes.
- Use Python code to add, read, update, or delete data in your database.

It's like a translator that lets you talk to your database using Python instead of SQL.

Using an ORM like SQLAlchemy offers several benefits:

1. **Easier to Use**
You write Python code instead of SQL, which is simpler and clearer.

2. **Less Repetition**
It does a lot of the work for you, so you don’t have to write the same code over and over.

3. **Works with Any Database**
You can easily switch databases (like SQLite or PostgreSQL) without changing much code.

4. **Safer**
It protects your app from security risks like SQL injection.

5. **Handles Relationships Easily**
It makes it simple to work with related data (like linking users to posts).

6. **Saves Time**
You can focus more on your app and less on writing complicated database queries.

7. **Simpler Data Management**
It lets you work with database data like normal Python objects, making it easier to manage.

8. **Team-Friendly**
Everyone in your team can follow the same approach to interact with the database.

## SQLAlchemy abstracts away the need for directly interacting with the database via cursors, SQL statements, or connection objects

1. **SQLAlchemy handles the database connection and querying for you**

    - SQLAlchemy manages database connections, queries, and results behind the scenes.
    - Instead of writing raw SQL queries and manually handling cursors, SQLAlchemy allows you to interact with the database using **Python objects** (like ``Student`` models in your case).
    - SQLAlchemy automatically generates the necessary SQL statements (e.g., ``SELECT``, ``INSERT``, ``UPDATE``, ``DELETE``) for you.

2. **SQLAlchemy's ORM abstracts away low-level database operations**

    - When you work with SQLAlchemy's ORM, you interact with **model instances** and **queries** rather than raw database cursors or SQL.
    - For example, instead of doing something like:

    ```python
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    cursor.close()
    ```

    You can do:

    ```python
    students = Student.query.all()  # Automatically generates the SQL and executes it
    ```

    - SQLAlchemy converts these high-level ORM operations into SQL under the hood and retrieves the results as Python objects (e.g., ``Student`` objects).

3. **SQLAlchemy handles result sets automatically**
    - When you use SQLAlchemy's ORM methods (e.g., ``query.all()``, ``query.get()``), the results are automatically returned as **model instances** that you can manipulate directly in Python.
    - For example:

    ```python
    students = Student.query.all()  # Returns a list of Student model instances
    ```

    - You don’t need to manually fetch rows with a cursor because SQLAlchemy will return the data in a convenient form as Python objects.
4. **Session-based interaction**
    - SQLAlchemy introduces the concept of a **session**, which is a layer that manages transactions and database operations.
    - Instead of using a cursor to execute queries directly, you interact with the **session** object, which tracks changes, handles the query lifecycle, and commits transactions automatically.
    Example of interacting with a session:

    ```python
    student = Student.query.get(1)  # Automatically fetches the student with id=1
    db.session.add(new_student)  # Adds a new student to the session
    db.session.commit()  # Commits the changes to the database
    ```

5. **Querying and managing the database with objects**
    - SQLAlchemy’s ORM allows you to use Python syntax to perform operations like querying, updating, and inserting data. It automatically translates your actions into SQL commands under the hood.
    - For example, inserting a new student becomes:

    ```python
    new_student = Student(first_name="John", last_name="Doe", email="john@example.com")
    db.session.add(new_student)  # Add to session
    db.session.commit()  # Save to database
    ```

    - No need for manually creating and executing SQL queries, or using a cursor to manage the result set.

## Install these dependencies

``pip install pymysql flask-sqlalchemy``
