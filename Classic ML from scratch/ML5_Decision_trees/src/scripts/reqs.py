import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from sklearn.preprocessing import OneHotEncoder
from sklearn import tree
from category_encoders import CountEncoder
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
import optuna

# from trash.oldshit import *
from scripts.DecisionTreeClassifier import *
from scripts.DecisionTreeRegressor import *
from scripts.RandomForestClassifier import *
from scripts.GBDTClassifier import *
from scripts.ExtraTreesClassifier import *
from scripts.preprocessing import *
from scripts.optuna import *


optuna.logging.set_verbosity(optuna.logging.WARNING)