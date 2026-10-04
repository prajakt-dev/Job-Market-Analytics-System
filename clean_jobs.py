import pandas as pd

# Read API data
df = pd.read_json("raw_jobs.json")

print("Original jobs:", len(df))

# Keep only useful columns
columns = [
    "id",
    "title",
    "company_name",
    "category",
    "job_type",
    "candidate_required_location",
    "salary",
    "publication_date",
    "url",
    "description"
]

df = df[columns]

# Remove duplicate jobs
df = df.drop_duplicates(subset=["id"])

# Clean text columns
text_columns = [
    "title",
    "company_name",
    "category",
    "job_type",
    "candidate_required_location",
    "salary"
]

for col in text_columns:
    df[col] = df[col].fillna("Not Specified").astype(str).str.strip()

# Convert publication date
df["publication_date"] = pd.to_datetime(
    df["publication_date"],
    errors="coerce"
)

# Create useful skill indicators
df["Python"] = df["description"].str.contains(
    "python", case=False, na=False
)

df["SQL"] = df["description"].str.contains(
    r"\bsql\b", case=False, na=False
)

df["Data_Science"] = df["description"].str.contains(
    "data science|data scientist",
    case=False,
    na=False
)

# Save cleaned data
df.to_csv("clean_jobs.csv", index=False)

print("Clean jobs:", len(df))

print("\nJobs requiring Python:")
print(df["Python"].sum())

print("\nJobs requiring SQL:")
print(df["SQL"].sum())

print("\nJobs requiring Data Science:")
print(df["Data_Science"].sum())

print("\nCleaned data saved as clean_jobs.csv")