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

```
export DATABASE_URL="sqlite+aiosqlite:///./mydb.db"
```

# PostgreSQL (asyncpg)

```
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"
```

# MySQL (aiomysql)

```
export DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/mydb"
```

# Getting Started with `asyncdjangoorm`

`asyncdjangoorm` is an asynchronous ORM inspired by Django, built on top of SQLAlchemy. It integrates easily with `aiogram` for Telegram bots.

---

## 1️⃣ Install the package

```bash
pip install asyncdjangoorm

```

---

## 2️⃣ Define Models

You can define your models using SQLAlchemy and attach `AsyncManager` for async operations.

```python
# models.py
from sqlalchemy import Column, Integer, String
from asyncdjangoorm import TimeStampedModel, AsyncManager

class MyModel(TimeStampedModel):
    __tablename__ = "my_model"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    value = Column(Integer)

# Attach AsyncManager
MyModel.objects = AsyncManager(MyModel)
```

> `TimeStampedModel` automatically adds `created_at` and `updated_at` fields.

---

## 3️⃣ Initialize the Database

Before using your models, initialize all tables:

```python
# init_db_example.py
import asyncio
from asyncdjangoorm import init_db
from models import MyModel

async def main():
    await init_db()  # Create all tables

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4️⃣ Using the ORM

Basic usage examples:

```python
# usage_example.py
import asyncio
from models import MyModel

async def main():
    # Create a new object
    await MyModel.objects.create(name="Test", value=42)

    # Fetch all objects
    items = await MyModel.objects.all()
    print(items)

    # Filter objects
    filtered = await MyModel.objects.filter(value__gt=10)
    print(filtered)

    # Get or create an object
    obj, created = await MyModel.objects.get_or_create(name="Example")
    print(obj, "Created:", created)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5️⃣ Integrating with aiogram

Example Telegram bot using `asyncdjangoorm`:

```python
# bot_example.py
import asyncio
from aiogram import Bot, Dispatcher, types
from asyncdjangoorm import init_db
from models import MyModel

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
    await init_db()  # Initialize tables

@dp.message_handler(commands=["create"])
async def create_item(message: types.Message):
    await MyModel.objects.create(name="FromBot", value=99)
    await message.answer("Item created!")

@dp.message_handler(commands=["list"])
async def list_items(message: types.Message):
    items = await MyModel.objects.all()
    text = "\n".join(f"{item.id}: {item.name} = {item.value}" for item in items) or "No items found."
    await message.answer(text)

if __name__ == "__main__":
    asyncio.run(on_startup())
    dp.run_polling(bot)
```

---

## 6️⃣ Notes

- `AsyncManager` allows **async CRUD operations**, filtering, ordering, and annotations.

- Compatible with **all Python 3 versions** and **aiogram 2.x and 3.x**.
- You can attach `AsyncManager` to any SQLAlchemy model.
