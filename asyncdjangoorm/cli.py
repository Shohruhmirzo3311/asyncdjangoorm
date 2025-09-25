import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Literal
from importlib.resources import files

PROJECT_TEMPLATES_DIR = files("asyncdjangoorm") / "project_template"

DBType = Literal["sqlite", "postgres", "mysql"]

DB_CHOICES = {
    "sqlite": {
        "driver": "sqlite+aiosqlite",
        "url_template": "sqlite+aiosqlite:///./{project_name}.db",
        "extra": "sqlite",
    },
    "postgres": {
        "driver": "postgresql+asyncpg",
        "url_template": "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}",
        "extra": "postgres",
    },
    "mysql": {
        "driver": "mysql+aiomysql",
        "url_template": "mysql+aiomysql://{user}:{password}@{host}:{port}/{db}",
        "extra": "mysql",
    },
}


def get_db_url(db: str, project_name: str) -> str:
    """Produce a sensible DB URL for chosen backend using env vars or defaults."""
    tpl = DB_CHOICES[db]["url_template"]
    if db == "sqlite":
        return tpl.format(project_name=project_name)
    if db == "postgres":
        return tpl.format(
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            db=os.getenv("POSTGRES_DB", project_name),
        )
    if db == "mysql":
        return tpl.format(
            user=os.getenv("MYSQL_USER", "user"),
            password=os.getenv("MYSQL_PASSWORD", "password"),
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=os.getenv("MYSQL_PORT", "3306"),
            db=os.getenv("MYSQL_DB", project_name),
        )
    raise ValueError("Unsupported db: " + str(db))


def _replace_placeholders(target_dir: Path, mapping: dict):
    """Replace textual placeholders in all text files under target_dir."""
    for root, _dirs, files in os.walk(target_dir):
        for fname in files:
            p = Path(root) / fname
            # skip obvious binary files by attempting text read
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            for k, v in mapping.items():
                text = text.replace(k, v)
            p.write_text(text, encoding="utf-8")


def _write_settings(target_dir: Path, project_name: str, db_url: str):
    settings_path = target_dir / "settings.py"
    settings_content = f"""# Generated settings for {project_name}
import os

PROJECT_NAME = "{project_name}"
# DATABASE_URL can be overridden by environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "{db_url}")

# Add your other defaults here (logging, token placeholders, etc.)
"""
    settings_path.write_text(settings_content, encoding="utf-8")


def _write_requirements(target_dir: Path, db_extra: str):
    text = f"""# Requirements for this project
asyncdjangoorm[{db_extra}]
"""
    (target_dir / "requirements.txt").write_text(text, encoding="utf-8")


def startproject(
    project_name: str,
    directory: str = ".",
    template: str = "simple",
    db: Optional[DBType] = None,
    bootstrap: bool = False,
):
    target_dir = Path(directory).resolve() / project_name
    if target_dir.exists():
        raise FileExistsError(f"Directory {target_dir} already exists!")

    tpldir = PROJECT_TEMPLATES_DIR 
    # copy template (we already ensured target doesn't exist)
    shutil.copytree(tpldir, target_dir)

    # replace placeholders in template files
    mapping = {"{{project_name}}": project_name}
    _replace_placeholders(target_dir, mapping)

    # choose DB
    if db is None:
        print("Select the database type:")
        print("1) sqlite (default)")
        print("2) postgres")
        print("3) mysql")
        choice = input("Enter choice (1-3): ").strip()
        db = {"1": "sqlite", "2": "postgres", "3": "mysql"}.get(choice, "sqlite")

    if db not in DB_CHOICES:
        raise ValueError("Unsupported db: " + str(db))

    db_url = get_db_url(db, project_name)
    _write_settings(target_dir, project_name, db_url)
    _write_requirements(target_dir, DB_CHOICES[db]["extra"])

    print(f"Project {project_name} created at {target_dir}")
    print("Next steps:")
    print(f"  cd {project_name}")
    print(
        f"  pip install -r requirements.txt   # or: pip install asyncdjangoorm[{DB_CHOICES[db]['extra']}]"
    )

    if bootstrap:
        confirm = input(
            "Bootstrap: create venv and pip install requirements? [y/N]: "
        ).strip().lower()
        if confirm == "y":
            venv_dir = target_dir / ".venv"
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
            pip_exec = venv_dir / "bin" / "pip"
            subprocess.check_call([str(pip_exec), "install", "-r", str(target_dir / "requirements.txt")])
            print("Bootstrapped virtualenv at", venv_dir)


