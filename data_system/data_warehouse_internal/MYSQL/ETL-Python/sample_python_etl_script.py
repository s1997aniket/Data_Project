import mysql.connector
import pandas as pd

# --------------------
# EXTRACT
# --------------------
def extract_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )

    query = "SELECT id, name, age, salary FROM users"
    df = pd.read_sql(query, conn)

    conn.close()
    return df


# --------------------
# TRANSFORM
# --------------------
def transform_data(df):
    # Remove rows with missing values
    df = df.dropna()

    # Filter: keep only users older than 25
    df = df[df["age"] > 25]

    # Add new column (example transformation)
    df["salary_band"] = df["salary"].apply(
        lambda x: "High" if x > 50000 else "Low"
    )

    return df


# --------------------
# LOAD
# --------------------
def load_data(df):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )

    cursor = conn.cursor()

    # Create target table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_cleaned (
            id INT,
            name VARCHAR(100),
            age INT,
            salary INT,
            salary_band VARCHAR(20)
        )
    """)

    # Insert data
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO users_cleaned (id, name, age, salary, salary_band)
            VALUES (%s, %s, %s, %s, %s)
        """, (row["id"], row["name"], row["age"], row["salary"], row["salary_band"]))

    conn.commit()
    conn.close()


# --------------------
# PIPELINE RUN
# --------------------
if __name__ == "__main__":
    print("Starting ETL pipeline...")

    data = extract_data()
    print("Extracted:", len(data), "rows")

    transformed = transform_data(data)
    print("Transformed:", len(transformed), "rows")

    load_data(transformed)
    print("Data loaded successfully into MySQL")

