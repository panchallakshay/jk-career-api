import os
import requests

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "Career QA Dataset.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/Career%20QA%20Dataset.csv",

    "CareerRecommenderDataset.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/CareerRecommenderDataset.csv",

    "Career_Database.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/Career_Database.csv",

    "Career_Enrichment_Data.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/Career_Enrichment_Data.csv",

    "Career_Knowledge_Master_JK_Augmented.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/Career_Knowledge_Master_JK_Augmented.csv",

    "JK_Career_Guidance_Master_Dataset.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/JK_Career_Guidance_Master_Dataset.csv",

    "JK_Colleges_Complete.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/JK_Colleges_Complete.csv",

    "JK_Entrance_Exams_Complete.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/JK_Entrance_Exams_Complete.csv",

    "JK_Scholarships_Complete.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/JK_Scholarships_Complete.csv",

    "JK_Skills_Development_Guide.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/JK_Skills_Development_Guide.csv",

    "Job Datsset.csv":
        "https://github.com/panchallakshay/jk-career-api/releases/download/v1/Job%20Datsset.csv"
}

def download_all():
    for filename, url in FILES.items():
        path = os.path.join(DATA_DIR, filename)

        if os.path.exists(path):
            print(f"✔ {filename} already exists")
            continue

        print(f"⬇ Downloading {filename} ...")
        r = requests.get(url)

        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✔ Downloaded {filename}")
        else:
            print(f"✖ Failed to download {filename}: {r.status_code}")

if __name__ == "__main__":
    download_all()
