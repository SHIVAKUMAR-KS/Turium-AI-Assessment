# Migration from SQLite to PostgreSQL

## Changes Made

### 1. Dependencies
- Added `psycopg2-binary>=2.9.9` to `requirements.txt`
- This is the PostgreSQL adapter for Python

### 2. Configuration (`app/config.py`)
- Removed `database_path` (SQLite-specific)
- Added PostgreSQL connection settings:
  - `postgres_host` (default: localhost)
  - `postgres_port` (default: 5432)
  - `postgres_user` (default: postgres)
  - `postgres_password` (default: postgres)
  - `postgres_db` (default: knowledge_inbox)
  - `database_url` (optional: full connection string)
- Added `get_database_url` property to construct PostgreSQL connection string

### 3. Database Setup (`app/database.py`)
- Changed from SQLite connection: `sqlite:///path/to/db.db`
- To PostgreSQL connection: `postgresql://user:password@host:port/database`
- Removed SQLite-specific code:
  - `os.makedirs()` for database directory
  - `check_same_thread=False` connection argument
- Added PostgreSQL connection pooling:
  - `pool_pre_ping=True` (verify connections)
  - `pool_size=5`
  - `max_overflow=10`

### 4. Environment Variables
- Updated `.env.example` with PostgreSQL configuration
- Supports both individual settings and full `DATABASE_URL`

## Setup Instructions

1. **Install PostgreSQL** (if not already installed)
   - See `backend/POSTGRES_SETUP.md` for detailed instructions

2. **Create Database**
   ```bash
   createdb knowledge_inbox
   # Or using psql:
   psql -U postgres -c "CREATE DATABASE knowledge_inbox;"
   ```

3. **Install Python Dependencies**
   ```bash
   pip install psycopg2-binary
   # Or reinstall all:
   pip install -r requirements.txt
   ```

4. **Update `.env` File**
   ```env
   OPENAI_API_KEY=your_key_here
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=knowledge_inbox
   ```

5. **Run Application**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Migration from Existing SQLite Database

If you have existing data in SQLite:

1. Export data from SQLite:
   ```bash
   sqlite3 data/knowledge_inbox.db .dump > sqlite_dump.sql
   ```

2. Convert and import to PostgreSQL (manual process):
   - SQLite and PostgreSQL have different SQL dialects
   - You may need to manually convert the dump file
   - Or use a migration tool like `pgloader`

3. Alternatively, start fresh with PostgreSQL (recommended for development)

## Benefits of PostgreSQL

- **Concurrent Connections**: Better handling of multiple users
- **Production Ready**: Industry-standard database
- **Scalability**: Better performance with large datasets
- **Advanced Features**: Full-text search, JSON support, etc.
- **Connection Pooling**: Efficient resource management

## Troubleshooting

### Connection Issues
- Verify PostgreSQL is running: `pg_isready`
- Check connection settings in `.env`
- Ensure database exists: `psql -l | grep knowledge_inbox`

### Permission Issues
- Grant privileges: `GRANT ALL ON DATABASE knowledge_inbox TO your_user;`
- Check `pg_hba.conf` for authentication settings

### Import Errors
- Ensure `psycopg2-binary` is installed
- Check Python version compatibility (Python 3.8+)


