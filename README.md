# AsyncDjangoORM

**AsyncDjangoORM** is an asynchronous ORM inspired by Django's ORM, built on top of SQLAlchemy.  
It provides Django-like Querysets and Managers, allowing you to work with SQL databases using Python `async/await`. Perfect for async frameworks like **aiogram**, **FastAPI**, or **Starlette**.

---

## Features

- Asynchronous database operations with `async/await`.
- Django-style `Queryset` and `AsyncManager`.
- Filter, exclude, order, annotate, aggregate, and bulk operations.
- `get`, `create`, `get_or_create`, `update_or_create`.
- `select_related` and `prefetch_related` for relational queries.
- Supports PostgreSQL, MySQL, and SQLite.
- Works seamlessly in async Python projects.

---

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

# Default: SQLite (works everywhere, no setup required)

DATABASE_URL = "sqlite+aiosqlite:///./asyncdjangoorm.db"

# PostgreSQL (asyncpg)

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"

# MySQL (aiomysql)

export DATABASE_URL="mysql+aiomysql://user:password@localhost:3306/mydb"

# SQLite (aiosqlite)

export DATABASE_URL="sqlite+aiosqlite:///./mydb.db"
