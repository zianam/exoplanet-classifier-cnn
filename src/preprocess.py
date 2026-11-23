
import json

import lightkurve as lk
import pandas as pd

from src.config import (
    PROCESSED_DIR,
    MASK_WIDTH_FACTOR,
    RAW_LIGHT_CURVE_DIR,
    FOLDED_LIGHT_CURVE_DIR,
    PROCESSED_FILE,
    LIGHT_CURVE_MISSION,
    LIGHT_CURVE_CADENCE
)


def load_light_curve(kepid: int, force_download: bool = False):

    RAW_LIGHT_CURVE_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_LIGHT_CURVE_DIR / f"KIC_{kepid}_{LIGHT_CURVE_CADENCE}_cadence.fits"

    if raw_path.exists() and not force_download:
        return lk.read(raw_path)

    search = lk.search_lightcurve(
    f"KIC {kepid}",
    mission=LIGHT_CURVE_MISSION,
    cadence=LIGHT_CURVE_CADENCE,
)

    if len(search) == 0:
        raise ValueError(f"No light curves found for KIC {kepid}")

    light_curves = search.download_all()

    if light_curves is None or len(light_curves) == 0:
        raise ValueError(f"Could not download light curves for KIC {kepid}")

    light_curve = light_curves.stitch().remove_nans()
    light_curve.to_fits(raw_path, overwrite=True)

    return light_curve


def flatten_and_fold(
    light_curve,
    period_days: float,
    epoch_bkjd: float,
    duration_days: float,
):
    if period_days <= 0 or duration_days <= 0:
        raise ValueError("Period and duration must be positive")

    mask_duration = duration_days * MASK_WIDTH_FACTOR

    transit_mask = light_curve.create_transit_mask(
        period=period_days,
        duration=mask_duration,
        transit_time=epoch_bkjd,
    )
    flattened = light_curve.flatten(mask=transit_mask)
    return flattened.fold(
        period=period_days,
        epoch_time=epoch_bkjd,
    )

def fold_tce(row, force_process=False):
    # Aligns repeated transits from multiple cycles into one folded light curve.
    kepid = int(row["kepid"])
    tce_number = int(row["tce_plnt_num"])

    period = float(row["tce_period"])
    epoch = float(row["tce_time0bk"])
    duration = float(row["tce_duration"]) / 24

    FOLDED_LIGHT_CURVE_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"KIC_{kepid}_TCE_{tce_number}"
    output_path = FOLDED_LIGHT_CURVE_DIR / f"{filename}.fits"
    metadata_path = FOLDED_LIGHT_CURVE_DIR / f"{filename}.json"

    if output_path.exists() and metadata_path.exists() and not force_process:
        return lk.read(output_path), duration, output_path

    light_curve = load_light_curve(kepid)
    folded = flatten_and_fold(light_curve, period, epoch, duration)

    metadata = {
        "kepid": kepid,
        "tce_plnt_num": tce_number,
        "period_days": period,
        "epoch_bkjd": epoch,
        "duration_days": duration,
        "mask_width_factor": MASK_WIDTH_FACTOR,
        "lightkurve_version": lk.__version__,
    }

    folded.to_fits(output_path, overwrite=True)
    metadata_path.write_text(json.dumps(metadata, indent=4))

    return folded, duration, output_path

def preprocess_catalog():
    tce_data = pd.read_csv(PROCESSED_DIR / PROCESSED_FILE)
    tce_data = tce_data.head(50)
    print(f"Starting preprocessing for {len(tce_data)} TCEs...")

    successful = 0
    failed = 0

    for index, row in tce_data.iterrows():
        try:
            _,_, output_path = fold_tce(row)
            successful += 1

            print(f"[{index + 1}/{len(tce_data)}] Processed: {output_path}")

        except Exception as e:
            failed += 1
            print(f"[{index + 1}/{len(tce_data)}] Failed KIC {row['kepid']}: {e}")

    print("\nPreprocessing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    preprocess_catalog()