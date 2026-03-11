from agentic_rag.memory.db import get_cursor


class ChatMemory:

    def create_session(self, session_id):

        cur = get_cursor()

        cur.execute(
            """
            INSERT INTO chat_sessions(session_id)
            VALUES(%s)
            ON CONFLICT DO NOTHING
            """,
            (session_id,)
        )

        cur.connection.commit()


    def add_message(self, session_id, role, content):

        cur = get_cursor()

        cur.execute(
            """
            INSERT INTO chat_messages(session_id, role, content)
            VALUES(%s,%s,%s)
            """,
            (session_id, role, content)
        )

        cur.connection.commit()


    def get_history(self, session_id):

        cur = get_cursor()

        cur.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE session_id=%s
            ORDER BY created_at
            """,
            (session_id,)
        )

        rows = cur.fetchall()

        history = []

        for r in rows:
            history.append({
                "role": r["role"],
                "content": r["content"]
            })

        return history