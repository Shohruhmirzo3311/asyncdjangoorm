# AsyncDjangoORM

**AsyncDjangoORM** is an asynchronous ORM inspired by Django's ORM, built on top of SQLAlchemy. It provides Django-like Querysets and AsyncManagers, allowing you to interact with databases using Python async/await.

## Ideal for telegram bots while building application with **aiogram**

## Features

Full async support using async/await.

Django-style Queryset and AsyncManager.

CRUD operations: get, create, get_or_create, update_or_create.

Query methods: filter, exclude, order_by, annotate, aggregate, bulk_create, bulk_update, bulk_delete.

Relation handling: select_related and prefetch_related.

Supports PostgreSQL, MySQL, and SQLite.

## Lightweight, flexible, and easy to integrate.

## Installation

Install via pip:

```bash
pip install asyncdjangoorm


# PostgreSQL
pip install asyncdjangoorm[postgres]

# MySQL
pip install asyncdjangoorm[mysql]

# SQLite (default)
pip install asyncdjangoorm[sqlite]
```

Database Configuration

# SQLite (default)

export DATABASE_URL="sqlite+aiosqlite:///./mydb.db"

# PostgreSQL (asyncpg)

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"

# MySQL (aiomysql)

export DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/mydb"

from asyncdjangoorm import AsyncManager
from your_models import MyModel # import your models

async def main(): # Fetch all objects asynchronously
objects = await MyModel.objects.all()
print(objects)

    # Create a new object
    await MyModel.objects.create(name="Test", value=42)

    # Get or create an object
    obj, created = await MyModel.objects.get_or_create(name="Example")

    # Filter objects
    filtered = await MyModel.objects.filter(value__gt=10)
