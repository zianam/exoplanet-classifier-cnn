"""Light-curve preprocessing: download, flatten and fold one TCE.

This is the one-star pipeline from the exploration notebook, moved into
functions. Binning into the global/local views and normalization are the
next steps and are not implemented here yet.
"""
import lightkurve as lk
from src.config import MASK_WIDTH_FACTOR


def load_light_curve(kepid: int):
    """Download every long-cadence quarter for a star and stitch them together.

    Returns a lightkurve LightCurve with NaNs removed. lightkurve caches the
    downloaded files, so repeat calls for the same star are faster.
    """
    search = lk.search_lightcurve(f"KIC {kepid}", mission="Kepler", cadence="long")
    if len(search) == 0:
        raise ValueError(f"No Kepler light curves found for KIC {kepid}")
    return search.download_all().stitch().remove_nans()


def flatten_and_fold(light_curve, period_days: float, epoch_bkjd: float,
                     duration_days: float):
    """Remove slow trends (ignoring the transits), then fold on the period.

    Args:
        light_curve: stitched lightkurve LightCurve.
        period_days: orbital period, in days.
        epoch_bkjd: time of one transit center, in BKJD.
        duration_days: transit duration, in DAYS (catalog value is in hours).

    Returns:
        The folded lightkurve LightCurve, with the transit centered at phase 0.
    """
    # True for measurements inside a transit; flatten() ignores them so the
    # dip is not fitted away.
    transit_mask = light_curve.create_transit_mask(
        period=period_days,
        duration=duration_days * MASK_WIDTH_FACTOR,
        transit_time=epoch_bkjd,
    )
    flattened = light_curve.flatten(mask=transit_mask)
    return flattened.fold(period=period_days, epoch_time=epoch_bkjd)


def fold_tce(row):
    """Download, flatten and fold the light curve for one row of the label table.

    Args:
        row: a row of tce_labels.csv (needs kepid, tce_period, tce_time0bk,
            tce_duration).

    Returns:
        (folded light curve, duration in days)
    """
    duration_days = row.tce_duration / 24  # catalog duration is in hours
    light_curve = load_light_curve(int(row.kepid))
    folded = flatten_and_fold(light_curve, row.tce_period, row.tce_time0bk,
                              duration_days)
    return folded, duration_days