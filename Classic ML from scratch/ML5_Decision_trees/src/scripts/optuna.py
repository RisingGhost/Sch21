from scripts.GBDTClassifier import *
from scripts.reqs import roc_auc_score, CatBoostClassifier, XGBClassifier, LGBMClassifier

def make_MyGBDT(X_train, y_train, X_val, y_val):
    def objective(trial):
        params = {
            "lr": trial.suggest_float("lr", 0.01, 0.15, log=True),
            "number_of_trees": trial.suggest_int("number_of_trees", 30, 150, step=10),
            "max_depth": trial.suggest_int("max_depth", 2, 5),
            "min_samples_split": trial.suggest_int("min_samples_split", 20, 100, step=10),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 10, 40, step=5),
            "max_features": True,
            # "n_bins": trial.suggest_int("n_bins", 32, 128, step=32),
            "random_state": 42,
        }

        model = GDBTClassifier(**params)
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_val)
        return roc_auc_score(y_val, proba)

    return objective

def make_MyGBDT_2(X_train, y_train, X_val, y_val):
    def objective(trial):
        params = {
            "lr": trial.suggest_float("lr", 0.08, 0.2, log=True),
            "number_of_trees": trial.suggest_int("number_of_trees", 120, 200, step=10),
            "max_depth": trial.suggest_int("max_depth", 4, 6),
            "min_samples_split": trial.suggest_int("min_samples_split", 80, 140, step=10),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 10, 25, step=5),
            "max_features": True,
            "n_bins": 128,
            "random_state": 42,
        }

        model = GDBTClassifier(**params)
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_val)
        return roc_auc_score(y_val, proba)

    return objective

def make_CatBoost(X_train, y_train, X_val, y_val, cat_cols=None):
    def objective(trial):



        params = {
            "iterations": trial.suggest_int("iterations", 50, 500, step=50),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "depth": trial.suggest_int("depth", 2, 10),
            "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 50),
            "rsm": trial.suggest_float("rsm", 0.3, 1.0),
            "random_seed": 42,
            "verbose": False,
        }


        model = CatBoostClassifier(**params)
        if cat_cols is not None:
            model.fit(X_train, y_train, cat_features=cat_cols)
        else:
            model.fit(X_train, y_train)

        proba = model.predict_proba(X_val)[:, 1]
        score = roc_auc_score(y_val, proba)

        return score
    return objective

def make_LightGBM(X_train, y_train, X_val, y_val):
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "max_depth": trial.suggest_int("max_depth", 2, 10),
            "min_child_samples": trial.suggest_int("min_child_samples", 1, 50),
            "feature_fraction": trial.suggest_float("feature_fraction", 0.3, 1.0),
            "random_state": 42,
            "verbosity": -1,
        }

        model = LGBMClassifier(**params)
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_val)[:, 1]
        score = roc_auc_score(y_val, proba)

        return score
    return objective

def make_XGBoost(X_train, y_train, X_val, y_val, cat_cols=None):
    def objective(trial):

        booster = trial.suggest_categorical("booster", ["gbtree", "dart"])
        params = {
            "booster": booster,
            "n_estimators": trial.suggest_int("n_estimators", 50, 300, step=50),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            "max_depth": trial.suggest_int("max_depth", 2, 10),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 50),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.3, 1.0),
            # "enable_categorical": True,
            "random_state": 42,
            "verbosity": 0,
        }

        if booster == "dart":
            params.update({
                "sample_type": trial.suggest_categorical("sample_type", ["uniform", "weighted"]),
                "normalize_type": trial.suggest_categorical("normalize_type", ["tree", "forest"]),
                "rate_drop": trial.suggest_float("rate_drop", 0.0, 0.5),
                "skip_drop": trial.suggest_float("skip_drop", 0.0, 0.5),
            })

        model = XGBClassifier(**params)
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_val)[:, 1]
        return roc_auc_score(y_val, proba)

    return objective