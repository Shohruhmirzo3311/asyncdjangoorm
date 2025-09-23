from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ext_modules = cythonize([
    Extension("asyncdjangoorm.queryset", ["asyncdjangoorm/queryset.py"]),
    Extension("asyncdjangoorm.manager", ["asyncdjangoorm/manager.py"]),
], compiler_directives={'language_level': "3"}, annotate=True)

setup(
    name="asyncdjangoorm",
    version="0.1.2",
    packages=find_packages(),
    license="MIT",
    author="Shohruhmirzo",
    author_email="jamoliddinovshohruh1@gmail.com",
    description="An asynchronous ORM inspired by Django's ORM, built on top of SQLAlchemy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    install_requires=[
        "SQLAlchemy>=2.0",
        "aiogram>=3.0",
    ],
    extras_require={
        "postgres": ["asyncpg"],
        "mysql": ["aiomysql"],
        "sqlite": [],
    },
    zip_safe=False,
    python_requires=">=3.12",
)
