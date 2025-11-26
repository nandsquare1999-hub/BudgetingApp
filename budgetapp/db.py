import duckdb

conn = duckdb.connect("budget.duckdb")

def next_id(table: str) -> int:
    row = conn.execute(f"SELECT COALESCE(MAX(id), 0) + 1 FROM {table}").fetchone()
    return row[0]

# Categories
conn.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    deleted BOOLEAN DEFAULT FALSE
);
""")

# Budget per month per category
conn.execute("""
CREATE TABLE IF NOT EXISTS budget_month_categories (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    month VARCHAR NOT NULL,
    budgeted INTEGER DEFAULT 0,
    spent INTEGER DEFAULT 0,
    balance INTEGER DEFAULT 0,
    deleted BOOLEAN DEFAULT FALSE
);
""")

# Transactions
conn.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE
);
""")
