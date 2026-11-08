import numpy as np
import pandas as pd
from src.config import *

TCE_events = pd.read_csv(RAW_DIR / CATALOG_FILE) 
TCE_copy = TCE_events.loc[TCE_events.av_training_set.isin(LABEL_MAP)].copy()
print(len(TCE_copy))  
OUT_FILE = PROCESSED_DIR / PROCESSED_FILE

TCE_copy["label"] = TCE_copy["av_training_set"].map(LABEL_MAP)
# print(TCE_copy.head())

def save_processed() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    TCE_copy.to_csv(OUT_FILE, index=False)

if __name__ == "__main__":
    save_processed()
    