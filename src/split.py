from sklearn.model_selection import GroupShuffleSplit
from config import RANDOM_SEED

groups = tce_data["kepid"].values

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.30,
    random_state=RANDOM_SEED
)

train_idx, temp_idx = next(splitter.split(X, y, groups=groups))

X_train, y_train = X[train_idx], y[train_idx]
X_temp, y_temp = X[temp_idx], y[temp_idx]
groups_temp = groups[temp_idx]

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=RANDOM_SEED
)

val_idx, test_idx = next(
    splitter.split(X_temp, y_temp, groups=groups_temp)
)

X_val, y_val = X_temp[val_idx], y_temp[val_idx]
X_test, y_test = X_temp[test_idx], y_temp[test_idx]