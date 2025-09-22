from setuptools import setup, find_packages

setup(
    name="asyncdjangoorm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=2.0",
        "aiogram>=3.0",
    ],
    extras_require={
        "postgres": ["asyncpg"],
        "mysql": ["aiomysql"],
        "sqlite": [],
    },
    python_requires=">=3.12",
)
