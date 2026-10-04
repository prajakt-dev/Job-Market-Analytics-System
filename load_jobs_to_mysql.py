import pandas as pd
import mysql.connector

# Read cleaned data
df = pd.read_csv("clean_jobs.csv")

print("Jobs to load:", len(df))

# Convert date
df["publication_date"] = pd.to_datetime(
    df["publication_date"],
    errors="coerce"
)

# Connect to MariaDB
connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Prajakt@123",
    database="job_market_db"
)

cursor = connection.cursor()

print("Connected to MariaDB!")

# Insert jobs
sql = """
INSERT INTO jobs (
    job_id, title, company_name, category, job_type,
    location, salary, publication_date, url, description,
    Python_Skill, SQL_Skill, Data_Science
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    cursor.execute(
        sql,
        (
            int(row["id"]),
            row["title"],
            row["company_name"],
            row["category"],
            row["job_type"],
            row["candidate_required_location"],
            row["salary"],
            row["publication_date"].date()
                if pd.notna(row["publication_date"])
                else None,
            row["url"],
            row["description"],
            bool(row["Python"]),
            bool(row["SQL"]),
            bool(row["Data_Science"])
        )
    )

connection.commit()

print("Jobs inserted:", len(df))

cursor.close()
connection.close()

print("Database connection closed.")