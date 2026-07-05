import sqlite3
from pathlib import Path

DB_FILE = "sample.db"


def create_database() -> None:
    # Create SQLite database and employees table with sample data
    db_path = Path(DB_FILE)
    
    # Remove existing database if present
    if db_path.exists():
        db_path.unlink()
    
    db_connection = sqlite3.connect(db_path)
    db_cursor = db_connection.cursor()
    
    # Create employees table
    db_cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            employee_id TEXT NOT NULL UNIQUE
        )
    """)
    
    # Insert sample data
    sample_data = [
        ("山田太郎", "営業部", "EMP001"),
        ("佐藤花子", "営業部", "EMP002"),
        ("鈴木一郎", "開発部", "EMP003"),
        ("田中美咲", "開発部", "EMP004"),
        ("高橋健太", "人事部", "EMP005"),
    ]
    
    db_cursor.executemany(
        "INSERT INTO employees (name, department, employee_id) VALUES (?, ?, ?)",
        sample_data
    )
    
    db_connection.commit()
    db_connection.close()
    
    print(f"Database created: {db_path.absolute()}")
    print(f"Total records inserted: {len(sample_data)}")


if __name__ == "__main__":
    create_database()
