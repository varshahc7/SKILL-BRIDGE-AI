from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "job_roles.csv"


def load_job_roles():
    """Load job role and skill data from the CSV file."""
    return pd.read_csv(DATA_PATH)


def get_job_role(data, role_name):
    """Find a job role by name."""
    matches = data[data["role"].str.lower() == role_name.strip().lower()]

    if matches.empty:
        return None

    return matches.iloc[0]


if __name__ == "__main__":
    data = load_job_roles()

    print("Dataset loaded successfully!")
    print(f"Number of job roles: {len(data)}")
    print("\nAvailable roles:")
    print(data["role"].to_string(index=False))