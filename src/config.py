from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CATALOG_COLUMNS = ["kepid", "tce_plnt_num", "tce_period", "tce_time0bk",
                   "tce_duration", "av_training_set"]
LABEL_MAP = {"PC": 1, "AFP": 0, "NTP": 0}