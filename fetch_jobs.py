import requests
import pandas as pd

url = "https://remotive.com/api/remote-jobs?category=software-dev&limit=50"

response = requests.get(url, timeout=20)

if response.status_code == 200:
    data = response.json()

    jobs = data["jobs"]

    df = pd.DataFrame(jobs)

    print("Jobs fetched:", len(df))
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 jobs:")
    print(df[["id", "title", "company_name", "category", "job_type"]].head())

    df.to_json("raw_jobs.json", orient="records", indent=2)

    print("\nSaved raw_jobs.json")

else:
    print("API Error:", response.status_code)