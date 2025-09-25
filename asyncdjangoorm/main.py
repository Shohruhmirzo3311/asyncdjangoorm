import sys
import argparse
from asyncdjangoorm.cli import startproject


def main():
    parser = argparse.ArgumentParser(
        prog="asyncdjangoorm",
        description="AsyncDjangoORM migration manager"
    )
    subparsers = parser.add_subparsers(dest="command")
    
    
    # Start project
    sp_start = subparsers.add_parser("startproject", help="Create a new project from template")
    sp_start.add_argument("name", help="Name of the project")
    sp_start.add_argument("-d", "--directory", default=".", help="Target directory")
    sp_start.add_argument("-t", "--template", default="simple", help="Template name (simple|full)")
    sp_start.add_argument("--db", choices=["sqlite", "postgres", "mysql"], help="Database backend")
    sp_start.add_argument("--bootstrap", action="store_true", help="Create venv and install requirements")


    # makemigrations
    makemigrations_parser = subparsers.add_parser("makemigrations", help="Create a new migration")
    makemigrations_parser.add_argument("message", nargs="?", default="auto migration")

    # migrate
    migrate_parser = subparsers.add_parser("migrate", help="Apply migrations")
    migrate_parser.add_argument("target", nargs="?", default="head")

    # rollback
    rollback_parser = subparsers.add_parser("rollback", help="Revert migrations")
    rollback_parser.add_argument("target", nargs="?", default="-1")
    
    

    args = parser.parse_args()
    
    if args.command == "startproject":
        startproject(
            project_name=args.name,
            directory=args.directory,
            template=args.template,
            db=args.db,
            bootstrap=args.bootstrap,
        )
    elif args.command == "makemigrations":
        from asyncdjangoorm.migrations.manager import makemigrations
        makemigrations(args.message)
    elif args.command == "migrate":
        from asyncdjangoorm.migrations.manager import migrate
        migrate(args.target)
    elif args.command == "rollback":
        from asyncdjangoorm.migrations.manager import rollback
        rollback(args.target)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()



# python -m asyncdjangoorm makemigrations "init"
# python -m asyncdjangoorm migrate
# python -m asyncdjangoorm rollback -1
