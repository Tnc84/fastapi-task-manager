# Changelog

## 2026-11-26 — Projects, comments, soft delete

### Soft delete (tasks & users)
- `DELETE /api/v1/tasks/{id}` and `DELETE /api/v1/users/{id}` are soft deletes (`deleted_at`); admin-only via `X-Actor-User-Id` (superuser).
- Admins cannot soft-delete their own user account.
- List/get endpoints hide soft-deleted rows by default.
- `include_deleted=true` is allowed only for admins (same actor header).
- Responses expose optional `deleted_at`.

### Projects
- New resource under `/api/v1/projects` (list, get, create, update, delete).
- Fields: `name`, `description`, `key` (unique, 2–10 chars).
- Tasks can be linked with optional `project_id`.
- Task list supports filter `?project_id=`.

### Comments
- Nested under tasks: `/api/v1/tasks/{task_id}/comments`.
- CRUD: list, create, update, delete.
- Create body: `content`, `author_id`.

### Task model / schema
- Added `status` (`todo` | `in_progress` | `done`).
- Added optional `project_id`.
- Task update can change `owner_id` and `project_id`.

### User schema
- `is_superuser` on create/update/response.
- Optional `deleted_at` on response.

### Startup schema sync
- `ensure_schema()` runs on app start (`app/core/db_migrate.py`).
- Creates missing tables (`projects`, `comments`) and columns (`tasks.status`, `tasks.project_id`, `tasks.deleted_at`, `users.deleted_at`).
- Prefer Alembic for production; this covers local/dev drift.

### CORS
- Added origins for Vite preview: `http://localhost:4173` and `http://127.0.0.1:4173`.

### Auth header used by admin actions
- Header: `X-Actor-User-Id: <user_id>`
- Required for soft delete and for `include_deleted=true`.
