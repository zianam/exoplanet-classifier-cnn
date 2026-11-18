import requests
from src.config import RAW_DIR, CATALOG_COLUMNS, CATALOG_FILE

TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

OUT_FILE = RAW_DIR / CATALOG_FILE
params = {
    "query": f"select {', '.join(CATALOG_COLUMNS)} from q1_q17_dr24_tce",
    "format": "csv",
}

def download_catalog() -> None:
    response = requests.get(TAP_URL, params = params, timeout=120)
    response.raise_for_status()

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(response.text)

    print(response.url)
    print(response.status_code)  
    print(f"Saved {OUT_FILE}")

if __name__ == "__main__":
    download_catalog()

