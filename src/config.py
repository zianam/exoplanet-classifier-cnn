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
RAW_LIGHT_CURVE_DIR = RAW_DIR / "light_curves"
FOLDED_LIGHT_CURVE_DIR = PROCESSED_DIR / "folded_light_curves"

# Preprocessing settings (from Shallue & Vanderburg 2018, except MASK_WIDTH_FACTOR)
GLOBAL_BINS = 2001
LOCAL_BINS = 201
LOCAL_NUM_DURATIONS = 4        # local view spans +/- 4 transit durations
GAP_THRESHOLD_DAYS = 0.75
MASK_WIDTH_FACTOR = 1.5        # our choice: mask 1.5x the duration when flattening
RANDOM_SEED = 42
LIGHT_CURVE_MISSION="Kepler"
LIGHT_CURVE_CADENCE = "long"