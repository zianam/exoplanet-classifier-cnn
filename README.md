# exoplanet-classifier-cnn

A 1D convolutional neural network that classifies Kepler threshold-crossing events as planet or non-planet from phase-folded light curves. A scaled-down replication of Shallue & Vanderburg (2018), including preprocessing (flattening, folding, global/local binning), model training, and precision/recall evaluation.

## Reproducing the Data

Run all commands from the repository root directory with your virtual environment active.

### 1. Environment Setup

Ensure your virtual environment is active and install the project dependencies:

```bash
# Activate your virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Download the DR24 TCE catalog from the Caltech TAP API to data/raw/
python -m src.download_catalog

# Clean, map training labels, and export processed catalog to data/processed/
python -m src.process_catalog
