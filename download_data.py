import os
import requests

BASE_URL = "https://github.com/panchallakshay/jk-career-api/releases/download/v1/"

DATASETS = {
    "Career.QA.Dataset.csv": "Career.QA.Dataset.csv",
    "CareerRecommenderDataset.csv": "CareerRecommenderDataset.csv",
    "Career_Database.csv": "Career_Database.csv",
    "Career_Enrichment_Data.csv": "Career_Enrichment_Data.csv",
    "Career_Knowledge_Master_JK_Augmented.csv": "Career_Knowledge_Master_JK_Augmented.csv",
    "JK_Career_Guidance_Master_Dataset.csv": "JK_Career_Guidance_Master_Dataset.csv",
    "JK_Colleges_Complete.csv": "JK_Colleges_Complete.csv",
    "JK_Entrance_Exams_Complete.csv": "JK_Entrance_Exams_Complete.csv",
    "JK_Scholarships_Complete.csv": "JK_Scholarships_Complete.csv",
    "JK_Skills_Development_Guide.csv": "JK_Skills_Development_Guide.csv",
    "Job.Dataset.csv": "Job.Dataset.csv"
}

def download_file(filename):
    url = BASE_URL + filename
    print(f"⬇ Downloading {filename} ...")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✔ Downloaded {filename}")
        else:
            print(f"✖ Failed to download {filename}: {response.status_code}")
    except Exception as e:
        print(f"✖ Error downloading {filename}: {e}")

if __name__ == "__main__":
    for filename in DATASETS:
        download_file(filename)

