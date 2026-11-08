from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CATALOG_COLUMNS = ["kepid", "tce_plnt_num", "tce_period", "tce_time0bk",
                   "tce_duration", "av_training_set"]
CATALOG_FILE = "dr24_TCE.csv"
PROCESSED_FILE = "dr24_TCE_with_labels"
LABEL_MAP = {"PC": 1, "AFP": 0, "NTP": 0}