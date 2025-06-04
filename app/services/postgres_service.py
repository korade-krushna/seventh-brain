import sqlalchemy

from app.models import Session

class PostgresService:
    def __init__(self):
        self.engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
        self.conn = self.engine.connect()

    def store_session(self, session: Session):
        self.conn.execute(
            """
            INSERT INTO sessions (id, user_id, name, content)
            VALUES (:id, :user_id, :name, :content)
            ON CONFLICT (id, user_id) DO UPDATE SET
                content = :content,
                updated_at = CURRENT_TIMESTAMP  
            """,
            {
                "id": session.id,
                "user_id": session.user_id,
                "name": session.name,
                "content": session.content
            }
        )
        self.conn.commit()

    def get_session(self, session_id: str):
        self.conn.execute("SELECT data FROM sessions WHERE id = %s", (session_id,))
        return self.conn.fetchone()[0]