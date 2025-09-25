# AsyncDjangoORM

AsyncDjangoORM is a modern, asynchronous ORM for Python, inspired by Django and powered by SQLAlchemy. It provides Django-style querying, automated migrations, and project scaffolding for rapid development of async applications.

---

Our mission is to make database management intuitive for developers of any experience level, providing clear structure, async-first design, and integrated automation.

---

## Table of Contents

- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Project Layout](#project-layout)
- [Configuration](#configuration)
- [Models](#models)
- [Migrations](#migrations)
- [Database Initialization](#database-initialization)
- [QuerySets & Managers](#querysets--managers)
- [Query Reference](#query-reference)
- [Relationships](#relationships)
- [Integration with Handlers](#integration-with-handlers)
- [Testing](#testing)
- [Advanced Topics](#advanced-topics)
- [FAQ](#faq)
- [Resources](#resources)

---

## Introduction

AsyncDjangoORM brings the power and simplicity of Django’s ORM to async Python projects. It is designed for use with frameworks like aiogram, FastAPI, and any environment that supports `async/await`. You get familiar Django-style querying, migrations, and project scaffolding, all with full async support.

---

## Quick Start

1. **Install AsyncDjangoORM and a database driver:**

   ```sh
   pip install asyncdjangoorm[sqlite]
   # or for PostgreSQL
   pip install asyncdjangoorm[postgres]
   # or for MySQL
   pip install asyncdjangoorm[mysql]
   ```

2. **Create a new project:**

   ```sh
   asyncdjangoorm-admin startproject myproject --db sqlite --bootstrap
   ```

3. **Configure your database in `settings.py`:**

   ```python
   DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
   ```

4. **Define your models in `models.py`:**

   ```python
   from sqlalchemy import Column, Integer, String
   from asyncdjangoorm import TimeStampedModel, AsyncManager

   class User(TimeStampedModel):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       username = Column(String, unique=True)
       email = Column(String, unique=True)
       age = Column(Integer)

   User.objects = AsyncManager(User)
   ```

5. **Run migrations:**

   ```sh
   asyncdjangoorm-admin makemigrations "initial"
   asyncdjangoorm-admin migrate
   ```

6. **Initialize the database tables:**

   ```python
   import asyncio
   from asyncdjangoorm import init_db

   async def main():
       await init_db()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

---

## Project Layout

A typical AsyncDjangoORM project structure:

```
myproject/
├── manage.py
├── settings.py
├── migrations/
│   └── ... (auto-generated migration scripts)
├── handlers/
│   └── ... (Telegram bot handlers or business logic)
├── models.py
├── requirements.txt
└── ...
```

- **manage.py**: Entry point for management commands.
- **settings.py**: Project configuration, including database URL.
- **migrations/**: Alembic-powered migration scripts.
- **handlers/**: Business logic, e.g., Telegram bot handlers.
- **models.py**: SQLAlchemy models with AsyncManager.
- **requirements.txt**: Python dependencies.

---

## Configuration

Set your database URL in `settings.py`:

```python
DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
# or for PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"
# or for MySQL
DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/dbname"
```

You can also use environment variables for configuration.

---

## Models

Models are defined using SQLAlchemy’s declarative syntax. Attach an `AsyncManager` to each model for Django-style querying.

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from asyncdjangoorm import TimeStampedModel, AsyncManager

class Group(TimeStampedModel):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class User(TimeStampedModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    age = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="users")

Group.users = relationship("User", back_populates="group")
User.objects = AsyncManager(User)
Group.objects = AsyncManager(Group)
```

> `TimeStampedModel` adds `created_at` and `updated_at` fields automatically.

---

## Migrations

AsyncDjangoORM uses Alembic for migrations. Migration scripts are auto-generated and stored in `migrations/`.

- **Create a migration:**

  ```sh
  asyncdjangoorm-admin makemigrations "add user model"
  ```

- **Apply migrations:**

  ```sh
  asyncdjangoorm-admin migrate
  ```

- **Rollback migrations:**

  ```sh
  asyncdjangoorm-admin rollback -1
  ```

---

## Database Initialization

Before using your models, initialize all tables:

```python
import asyncio
from asyncdjangoorm import init_db

async def main():
    await init_db()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## QuerySets & Managers

AsyncDjangoORM provides Django-style querying via `AsyncManager` and `QuerySet`. All queries are async and return awaitable results.

### Basic Queries

```python
# Create
user = await User.objects.create(username="alice", email="alice@example.com", age=25)

# Get
user = await User.objects.get(username="alice")

# Get or Create
user, created = await User.objects.get_or_create(username="bob", defaults={"age": 30})

# Update or Create
user, created = await User.objects.update_or_create(
    username="charlie", defaults={"age": 35}
)
```

### Filtering & Excluding

```python
users = await User.objects.filter(age__gte=18).all()
users = await User.objects.exclude(username="alice").all()
```

### Ordering

```python
users = await User.objects.order_by("-age").all()
```

### Aggregation & Annotation

```python
total = await User.objects.aggregate(total_age=("age", "sum"))
```

### Bulk Operations

```python
await User.objects.bulk_create([
    {"username": "dave", "email": "dave@example.com", "age": 40},
    {"username": "eve", "email": "eve@example.com", "age": 22},
])

await User.objects.filter(age__lt=30).bulk_update({"age": 30})
await User.objects.filter(age__lt=20).bulk_delete()
```

---

## Query Reference

| Method                | Description                                     |
| --------------------- | ----------------------------------------------- |
| `.all()`              | Return all records                              |
| `.get(**kwargs)`      | Get a single record by fields                   |
| `.filter(**kwargs)`   | Filter records (supports Django-style lookups)  |
| `.exclude(**kwargs)`  | Exclude records                                 |
| `.order_by(*fields)`  | Order results                                   |
| `.aggregate()`        | Aggregate values (sum, avg, min, max, count)    |
| `.annotate()`         | Annotate results with calculated fields         |
| `.bulk_create()`      | Create multiple records                         |
| `.bulk_update()`      | Update multiple records                         |
| `.bulk_delete()`      | Delete multiple records                         |
| `.select_related()`   | Join related models (foreign keys)              |
| `.prefetch_related()` | Prefetch related models (many-to-many, reverse) |

**Django-style lookups supported:**  
`exact`, `iexact`, `contains`, `icontains`, `in`, `gt`, `gte`, `lt`, `lte`, `startswith`, `istartswith`, `endswith`, `iendswith`, `range`, `isnull`, etc.

---

## Relationships

AsyncDjangoORM supports SQLAlchemy relationships. Use `select_related` for foreign keys and `prefetch_related` for many-to-many or reverse relations.

```python
users = await User.objects.select_related("group").filter(group__name="Admins").all()
groups = await Group.objects.prefetch_related("users").all()
```

---

## Integration with Handlers

Use your models directly in async handlers (e.g., aiogram):

```python
from aiogram import types
from models import User

@dp.message_handler(commands=["register"])
async def register_user(message: types.Message):
    await User.objects.create(
        username=message.from_user.username,
        email="user@example.com",
        age=20
    )
    await message.answer("User registered!")

@dp.message_handler(commands=["list"])
async def list_users(message: types.Message):
    users = await User.objects.order_by("-age").all()
    text = "\n".join(f"{user.id}: {user.username} ({user.age})" for user in users)
    await message.answer(text or "No users found.")
```

---

## Testing

AsyncDjangoORM is compatible with pytest and other async test runners. Use fixtures to set up test databases and models.

```python
import pytest
from models import User

@pytest.mark.asyncio
async def test_user_creation():
    user = await User.objects.create(username="test", email="test@example.com", age=99)
    assert user.username == "test"
```

---

## Advanced Topics

- **Custom Managers:**  
  Subclass `AsyncManager` for reusable query logic.

- **Transactions:**  
  Use SQLAlchemy’s async session for atomic operations.

- **Raw SQL:**  
  Execute raw SQL queries via SQLAlchemy if needed.

- **Signals & Hooks:**  
  Implement custom hooks for model events (coming soon).

---

## FAQ

**Which Python versions are supported?**  
Python 3.7 and above.

**Can I use this with aiogram, FastAPI, or other async frameworks?**  
Yes, AsyncDjangoORM is compatible with any async Python framework.

**How do I manage migrations?**  
Use the CLI commands: `makemigrations`, `migrate`, `rollback`.

**Can I use raw SQL?**  
Yes, you can use SQLAlchemy’s core features for raw queries.

---

## Resources

- [Project Template](asyncdjangoorm/project_template/README.md)
- [Quick Start Example](asyncdjangoorm/examples/quick_start.py)
- [Migration Manager](asyncdjangoorm/migrations/manager.py)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [Django ORM Reference](https://docs.djangoproject.com/en/4.2/topics/db/queries/)

---

AsyncDjangoORM makes async database management simple, robust, and familiar for Python developers.  
For more examples and advanced usage, see the [examples](asyncdjangoorm/examples/) directory.

---
