"""
Lightweight startup migrations for schema drift.
"""

from sqlalchemy import inspect, text

from app.core.database import Base, engine
from app.models import Comment, Project, Task, User  # noqa: F401


def ensure_schema() -> None:
    """Create missing tables and columns required by the app."""
    Base.metadata.create_all(bind=engine)
    ensure_task_status_column()
    ensure_task_project_id_column()
    ensure_deleted_at_columns()


def ensure_deleted_at_columns() -> None:
    """Add soft-delete columns when missing."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "tasks" in tables:
        task_columns = {column["name"] for column in inspector.get_columns("tasks")}
        if "deleted_at" not in task_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE tasks ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE"))

    if "users" in tables:
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "deleted_at" not in user_columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE"))


def ensure_task_status_column() -> None:
    """Add tasks.status if missing and backfill from is_completed."""
    inspector = inspect(engine)
    if "tasks" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("tasks")}
    if "status" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE tasks ADD COLUMN status VARCHAR DEFAULT 'todo'")
        )
        connection.execute(
            text("UPDATE tasks SET status = 'done' WHERE is_completed = true")
        )
        connection.execute(
            text(
                "UPDATE tasks SET status = 'todo' "
                "WHERE is_completed = false OR is_completed IS NULL"
            )
        )


def ensure_task_project_id_column() -> None:
    """Add tasks.project_id if missing."""
    inspector = inspect(engine)
    if "tasks" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("tasks")}
    if "project_id" in columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE tasks ADD COLUMN project_id INTEGER"))
