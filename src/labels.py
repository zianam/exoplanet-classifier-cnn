import numpy as np
import pandas as pd
from src.config import *


def load_labels():
    catalog_path = RAW_DIR / CATALOG_FILE
    if not catalog_path.exists():
        raise FileNotFoundError(
            f"{catalog_path} not found. Run `python -m src.download_catalog` first."
        )
    TCE_events = pd.read_csv(catalog_path) 
    TCE_copy = TCE_events.loc[TCE_events.av_training_set.isin(LABEL_MAP)].copy()
    print(len(TCE_copy))  
    TCE_copy["label"] = TCE_copy["av_training_set"].map(LABEL_MAP)
    return TCE_copy
# print(TCE_copy.head())


def save_processed() -> None:
    OUT_FILE = PROCESSED_DIR / PROCESSED_FILE
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    TCE_copy = load_labels()
    TCE_copy.to_csv(OUT_FILE, index=False)


if __name__ == "__main__":
    save_processed()
    