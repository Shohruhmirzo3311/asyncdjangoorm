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

Getting Started

1. Initialize the Database

Before interacting with models, initialize your database tables. This ensures all models are properly created.

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from asyncdjangoorm import init_db
from models import MyModel
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Optional: set commands in Telegram menu

async def set_commands(bot: Bot):
await bot.set_my_commands([
BotCommand(command="create", description="Create a new item"),
BotCommand(command="list", description="List all items")
])

# Startup callback to initialize database and bot commands

async def on_startup():
await init_db() # Initialize all tables
await set_commands(bot)
print("Bot is ready and database initialized!")

# Example command handlers

@dp.message(commands=["create"])
async def cmd_create(message):
await MyModel.objects.create(name="FromBot", value=99)
await message.answer("Item created!")

@dp.message(commands=["list"])
async def cmd_list(message):
items = await MyModel.objects.all()
text = "\n".join(f"{item.id}: {item.name} = {item.value}" for item in items) or "No items found."
await message.answer(text)

if **name** == "**main**":
dp.run_polling(bot, on_startup=on_startup)

2. Define Models
   from sqlalchemy import Column, Integer, String
   from asyncdjangoorm import TimeStampedModel, AsyncManager

class MyModel(TimeStampedModel):
**tablename** = "my_model"
id = Column(Integer, primary_key=True)
name = Column(String, unique=True)
value = Column(Integer)

# Attach async manager

MyModel.objects = AsyncManager(MyModel)

3. Using the ORM

import asyncio
from models import MyModel

async def main(): # Fetch all objects
objects = await MyModel.objects.all()
print(objects)

    # Create a new object
    await MyModel.objects.create(name="Test", value=42)

    # Get or create an object
    obj, created = await MyModel.objects.get_or_create(name="Example")
    print(obj, created)

    # Filter objects
    filtered = await MyModel.objects.filter(value__gt=10)
    print(filtered)

if **name** == "**main**":
asyncio.run(main())

4. Integration with AIogram

import asyncio
from aiogram import Bot, Dispatcher, types
from asyncdjangoorm import init_db
from models import MyModel

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
await init_db() # Make sure tables exist

@dp.message_handler(commands=["create"])
async def create_item(message: types.Message):
await MyModel.objects.create(name="FromBot", value=99)
await message.answer("Item created!")

@dp.message_handler(commands=["list"])
async def list_items(message: types.Message):
items = await MyModel.objects.all()
text = "\n".join(f"{item.id}: {item.name} = {item.value}" for item in items)
await message.answer(text)

if **name** == "**main**":
asyncio.run(on_startup())
dp.run_polling(bot)
