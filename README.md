# exoplanet-classifer-cnn
A 1D convolutional neural network that classifies Kepler threshold-crossing events as planet or non-planet from phase-folded light curves. A scaled-down replication of Shallue &amp; Vanderburg (2018), including preprocessing (flattening, folding, global/local binning), model training, and precision/recall evaluation.


## Reproducing the data
Run all commands from the repo root with the virtual environment active.

1. python -m src.download_catalog   # downloads the DR24 TCE catalog to data/raw/