import pandas as pd
import mysql.connector

#connect to MariaDB
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Prajakt@123",
    database="job_market_db"
)

print("Connected to MariaDB!")

#read complete job data from the database
df = pd.read_sql("SELECT * FROM jobs", conn)

# total jobs
total_jobs = len(df)

# skill demand analysis
skill_demand = pd.DataFrame({
    "Skill": ["Python", "SQL", "Data Science"],
    "Job_Count": [
        df["Python_Skill"].sum(),
        df["SQL_Skill"].sum(),
        df["Data_Science"].sum()
    ]
})

# Analysis 3: Jobs by company
company_jobs = (
    df.groupby("company_name")
      .size()
      .reset_index(name="Job_Count")
      .sort_values("Job_Count", ascending=False)
)

# Analysis 4: Jobs by type
job_types = (
    df.groupby("job_type")
      .size()
      .reset_index(name="Job_Count")
      .sort_values("Job_Count", ascending=False)
)

# Analysis 5: Jobs by category
categories = (
    df.groupby("category")
      .size()
      .reset_index(name="Job_Count")
      .sort_values("Job_Count", ascending=False)
)

# Create Excel report
with pd.ExcelWriter("job_market_report.xlsx", engine="openpyxl") as writer:

    df.to_excel(writer, sheet_name="All_Jobs", index=False)

    skill_demand.to_excel(
        writer,
        sheet_name="Skill_Demand",
        index=False
    )

    company_jobs.to_excel(
        writer,
        sheet_name="Company_Analysis",
        index=False
    )

    job_types.to_excel(
        writer,
        sheet_name="Job_Types",
        index=False
    )

    categories.to_excel(
        writer,
        sheet_name="Categories",
        index=False
    )

print("\n===== JOB MARKET ANALYSIS =====")
print("Total Jobs:", total_jobs)

print("\nSkill Demand:")
print(skill_demand)

print("\nTop Companies:")
print(company_jobs.head(10))

print("\nJob Types:")
print(job_types)

print("\nExcel report created: job_market_report.xlsx")

conn.close()
print("\nDatabase connection closed.")