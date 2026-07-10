## Troubleshooting: `sqlalchemy.exc.ProgrammingError: can't adapt type 'HttpUrl'`

### Issue Description

When attempting to save a URL validated by Pydantic's `HttpUrl` type directly into a PostgreSQL database via SQLAlchemy, the application crashes with the following error:
`sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'HttpUrl'`

### Root Cause

Pydantic's `HttpUrl` is an object, not a raw string. The underlying PostgreSQL driver (`psycopg2`) does not natively understand how to serialize or "adapt" this special Pydantic object into a standard SQL `VARCHAR` or `TEXT` column.

### Solution / Fix

Always explicitly cast the Pydantic `HttpUrl` field to a Python string (`str`) before initializing or assigning it to the SQLAlchemy model in your CRUD operations or route handlers.

#### Incorrect Code (Do not do this):

```python
# Fails because request_data.url is an HttpUrl object
db_record = URL(original_url=request_data.url)
```

#### Correct Code:

```python
# Fixed by casting the validated URL object to a standard string
db_record = URL(original_url=str(request_data.url))
```

### Prevention / Guidelines

- **Schemas vs. Models:** Keep using `HttpUrl` in Pydantic schemas (`BaseModel`) to leverage robust data validation on API requests.
- **Database Operations:** Ensure any network types (`HttpUrl`, `EmailStr`, `IPvAnyAddress`) are parsed into plain Python primitives (`str`, `int`) before interacting with the database layer.
