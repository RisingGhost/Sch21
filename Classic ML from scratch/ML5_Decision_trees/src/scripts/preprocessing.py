from scripts.reqs import pd
from scripts.reqs import np
from scripts.reqs import precision_score, recall_score, f1_score, roc_auc_score

def __init__(self):
    pass

def make_date_features(df, date_col):

    result = pd.DataFrame(index=df.index)
    dt = pd.to_datetime(df[date_col])

    month = dt.dt.month
    result["PurchMonth_cos"] = np.cos(2*np.pi*month/12)
    result["PurchMonth_sin"] = np.sin(2*np.pi*month/12)

    day = dt.dt.dayofweek
    result["PurchDayOfWeek_cos"] = np.cos(2*np.pi*day/7)
    result["PurchDayOfWeek_sin"] = np.sin(2*np.pi*day/7)
    
    return result

def gini(roc):
    return 2*roc - 1

def show_metrics(y_true, y_pred=None, y_proba=None, threshold=0.5):
    if y_pred is None:
        y_pred = (y_proba >= threshold).astype(int)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    gini_score = 2 * roc_auc_score(y_true, y_proba) - 1

    metrics = {
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Gini": gini_score,
    }

    print(f'Precision: {precision:.4f}')
    print(f'Recall:    {recall:.4f}')
    print(f'F1:        {f1:.4f}')
    print(f'Gini:      {gini_score:.4f}')

    return metrics