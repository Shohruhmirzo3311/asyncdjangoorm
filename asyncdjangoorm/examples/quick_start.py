import asyncio

import sqlalchemy as sa

from asyncdjangoorm._internal.manager import AsyncManager
from asyncdjangoorm.config.base import Base
from asyncdjangoorm.config.init_tables import init_db


# Define a model
class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    age = sa.Column(sa.Integer, nullable=True)

    objects = AsyncManager(model=__qualname__)

async def main():
    await init_db()

    # Create
    user = await User.objects.create(username="john", email="john@example.com", age=25)
    print("Created:", user.username)

    # Get
    user = await User.objects.get(username="john")
    print("Retrieved:", user.username, user.email)

    # Filter
    users = await User.objects.filter(age__gte=18).all()
    for u in users:
        print("Filtered:", u.username)

    # Update
    await User.objects.filter(username="john").update(email="new@example.com")

    # Delete
    await User.objects.filter(username="john").delete()

if __name__ == "__main__":
    asyncio.run(main())
