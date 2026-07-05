import sqlite3
from pathlib import Path

from langchain_core.tools import tool

DB_FILE = "sample.db"
SYSTEM_PROMPT = """あなたはSQLiteデータベースの専門家アシスタントです。

重要な制約：
- データベースは読み取り専用です
- SELECT クエリのみ実行可能です
- 必ず日本語で回答してください

回答手順：
1. 質問内容を理解したら、まずテーブル一覧を確認
2. 必要に応じてスキーマを確認
3. 適切なSELECTクエリを実行
4. 結果を日本語でわかりやすく説明"""


@tool
def sql_db_list_tables() -> str:
    """List all tables in the database."""
    db_path = Path(DB_FILE)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    connection.close()
    return ", ".join([table[0] for table in tables])


@tool
def sql_db_schema(table_names: str) -> str:
    """Get schema information for specified tables (comma-separated)."""
    db_path = Path(DB_FILE)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    table_list = [name.strip() for name in table_names.split(",")]
    schema_info = []
    
    for table_name in table_list:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema_info.append(f"Table: {table_name}")
        for col in columns:
            schema_info.append(f"  - {col[1]} ({col[2]})")
    
    connection.close()
    return "\n".join(schema_info)


@tool
def sql_db_query(query: str) -> str:
    """Execute a SQL query and return results. Only SELECT queries are allowed."""
    # Safety guard: only allow SELECT statements
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed"
    
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            return f"Error: {keyword} statements are not allowed"
    
    db_path = Path(DB_FILE)
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        
        if not results:
            return "No results found"
        
        return str(results)
    except Exception as e:
        return f"Error executing query: {str(e)}"


SQL_TOOLS = [sql_db_list_tables, sql_db_schema, sql_db_query]