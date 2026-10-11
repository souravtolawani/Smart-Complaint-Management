

import sqlite3

DATABASE = "complaints.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_complaint(title, category, priority, description):
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO complaints
        (title, category, priority, description, status)
        VALUES (?, ?, ?, ?, ?)
    """, (title, category, priority, description, "Pending"))

    conn.commit()
    conn.close()


def get_complaints():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT * FROM complaints
        ORDER BY id DESC
    """).fetchall()

    complaints = [dict(row) for row in rows]
    conn.close()

    return complaints


if __name__ == "__main__":
    init_db()
    print("Database created successfully!")


def update_complaint_status(complaint_id, new_status):
    allowed_statuses = {"Pending", "In Progress", "Resolved"}

    if new_status not in allowed_statuses:
        return False

    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (new_status, complaint_id)
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated
