# PostgreSQL Setup Guide

## Prerequisites

1. Install PostgreSQL on your system:
   - **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - **macOS**: `brew install postgresql`
   - **Linux**: `sudo apt-get install postgresql` (Ubuntu/Debian) or `sudo yum install postgresql` (CentOS/RHEL)

2. Start PostgreSQL service:
   - **Windows**: PostgreSQL service should start automatically
   - **macOS**: `brew services start postgresql`
   - **Linux**: `sudo systemctl start postgresql`

## Database Setup

### Option 1: Using psql command line

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE knowledge_inbox;

# Create user (optional, if not using default postgres user)
CREATE USER knowledge_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE knowledge_inbox TO knowledge_user;

# Exit psql
\q
```

### Option 2: Using createdb command

```bash
createdb -U postgres knowledge_inbox
```

## Environment Configuration

Update your `.env` file with PostgreSQL connection details:

```env
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=knowledge_inbox

# Or use full URL format:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/knowledge_inbox
```

## Install Python Dependencies

```bash
pip install psycopg2-binary
```

## Verify Connection

Test the connection:

```python
from app.config import settings
from app.database import engine

# Test connection
with engine.connect() as conn:
    print("✓ PostgreSQL connection successful!")
```

## Troubleshooting

### Connection refused
- Ensure PostgreSQL service is running
- Check that `POSTGRES_HOST` and `POSTGRES_PORT` are correct

### Authentication failed
- Verify username and password in `.env`
- Check PostgreSQL `pg_hba.conf` allows your connection method

### Database does not exist
- Create the database using the commands above
- Verify `POSTGRES_DB` matches the created database name

### Permission denied
- Ensure the user has privileges on the database
- Grant necessary permissions: `GRANT ALL PRIVILEGES ON DATABASE knowledge_inbox TO your_user;`


