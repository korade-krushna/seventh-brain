from sqlalchemy import create_engine, text
from datetime import datetime

def create_sessions_table():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sessions (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL,
        content JSONB,
        created_at INTEGER DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP),
        updated_at INTEGER DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)
    );
    """
    
    create_index_sql = """
    CREATE INDEX IF NOT EXISTS idx_sessions_user_updated 
    ON sessions(user_id, updated_at DESC);
    """

    add_column_sql = """
    ALTER TABLE sessions ADD COLUMN IF NOT EXISTS name TEXT;
    """

    create_unique_index_sql = """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_sessions_id_user_id
    ON sessions(id, user_id);
    """
    
    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.execute(text(create_index_sql))
        connection.execute(text(add_column_sql))
        connection.execute(text(create_unique_index_sql))
        connection.commit()

if __name__ == "__main__":
    create_sessions_table()
