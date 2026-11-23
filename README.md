# exoplanet-classifier-cnn

A 1D CNN that classifies Kepler threshold-crossing events (TCEs) as planet or
non-planet from phase-folded light curves. A scaled-down replication of
Shallue & Vanderburg (2018), "Identifying Exoplanets with Deep Learning."

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Reproducing the data

Run every command from the repo root with the virtual environment active.

1. `python -m src.download_catalog`  downloads the DR24 TCE catalog to `data/raw/`
2. `python -m src.labels`            builds `data/processed/tce_labels.csv`
3. `python -m src.preprocess`  downloads and preprocesses the light curves for each TCE.



Expected after step 2: 15,737 labeled TCEs (3,600 PC, 9,596 AFP, 2,541 NTP),
i.e. 3,600 with `label` = 1 and 12,137 with `label` = 0.

Preprocessing: Each TCE is processed independently using its host star's original light curve. The pipeline:
Downloads and caches the original light curve for each star, reusing it when processing additional TCEs from that star.

Masks the expected transit regions using the TCE's period, duration, and epoch.
Flattens the light curve to remove long-term brightness trends while protecting the expected transits.
Folds the flattened light curve using the TCE's period and epoch, aligning repeated transits into one cycle.
Saves the resulting folded light curve as a FITS file and its processing parameters as a JSON metadata file.
Each TCE therefore produces its own folded light curve, even when multiple TCEs belong to the same star.

## Layout

```
src/
  config.py            shared paths and settings
  download_catalog.py  fetch the catalog from the NASA Exoplanet Archive
  labels.py            filter to labeled TCEs, add the binary label
  preprocess.py        download, flatten and fold light curves
notebooks/             exploration and plots (logic stays in src/)
data/                  not committed; created by the scripts
```

## Units

`tce_period` is in days, `tce_time0bk` is in BKJD, and `tce_duration` is in
**hours** (divide by 24 before using it with times in days).
 `tce_duration` is in hours and must be divided by 24 before using it with times in days.

## Deviations from the paper

- Smaller subset of the catalog (planned).
- Light curves fetched with lightkurve; flattening uses lightkurve's
  `flatten` with transits masked, not the paper's BIC-selected spline.
- Train/val/test split grouped by star (planned).
- Binned arrays saved as `.npz`; modern framework instead of TensorFlow 1.