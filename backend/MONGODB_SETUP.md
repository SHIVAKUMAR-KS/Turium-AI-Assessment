# MongoDB Setup Guide

## Prerequisites

1. Install MongoDB on your system:

   - **Windows**: Download from [mongodb.com/download](https://www.mongodb.com/try/download/community)
   - **macOS**: `brew install mongodb-community`
   - **Linux**: Follow [MongoDB installation guide](https://www.mongodb.com/docs/manual/installation/)

2. Start MongoDB service:
   - **Windows**: MongoDB service should start automatically, or run `net start MongoDB`
   - **macOS**: `brew services start mongodb-community`
   - **Linux**: `sudo systemctl start mongod`

## Python Dependencies

Install MongoDB Python drivers:

```bash
pip install motor pymongo
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Update your `.env` file with MongoDB connection details:

```env
# MongoDB Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=  # Optional, leave empty if no authentication
MONGODB_PASSWORD=  # Optional, leave empty if no authentication
MONGODB_DB=knowledge_inbox

# Or use full URL format:
# MONGODB_URL=mongodb://localhost:27017/knowledge_inbox
# MONGODB_URL=mongodb://user:password@localhost:27017/knowledge_inbox?authSource=admin
```

## Verify Connection

Test the connection:

```python
from app.database import init_db
init_db()
print("MongoDB connected successfully!")
```

## Database Structure

The application uses a single collection:

- **Collection**: `content_items`
- **Fields**:
  - `_id`: ObjectId (auto-generated)
  - `content`: string (text content)
  - `source_type`: string ("text" or "url")
  - `source_url`: string | null
  - `metadata`: string | null
  - `created_at`: datetime

## Troubleshooting

### Connection refused

- Ensure MongoDB service is running
- Check that `MONGODB_HOST` and `MONGODB_PORT` are correct
- Default: `localhost:27017`

### Authentication failed

- Verify username and password in `.env`
- Check MongoDB authentication settings
- Ensure user has read/write permissions on the database

### Database not found

- MongoDB creates databases automatically on first write
- No need to manually create the database

### Module not found

- Install dependencies: `pip install motor pymongo`
- Ensure virtual environment is activated

## Benefits of MongoDB

- **No Schema**: Flexible document structure
- **Easy Setup**: No migrations or table creation needed
- **Native JSON**: Perfect for API responses
- **Scalable**: Handles large datasets efficiently
- **Simple**: No complex joins or relationships needed for this use case
