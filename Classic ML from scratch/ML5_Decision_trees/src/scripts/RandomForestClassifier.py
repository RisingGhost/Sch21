from scripts.reqs import np
from scripts.DecisionTreeClassifier import *

class MyRandomForestClassifier:

    def __init__(self, n_estimators=100, max_depth=7, min_samples_split=50, min_samples_leaf=10, random_state=42):
        self.n_estimators=n_estimators
        self.max_depth=max_depth
        self.min_samples_split=min_samples_split
        self.min_samples_leaf=min_samples_leaf
        self.random_state=random_state
        self.rng = np.random.default_rng(random_state)

    def fit(self, X, y):
        self.X = np.array(X, dtype=np.float32)
        self.y = np.array(y, dtype=np.uint8)
        self.trees = []
        for _ in range(self.n_estimators):
            X_b, y_b = self._Bootstrap(self.X, self.y)
            tree = self._maketree()
            tree.fit(X_b, y_b)

            self.trees.append(tree)

    def _maketree(self):
        return MyDecisionTreeClassifier(self.max_depth, self.min_samples_split, self.min_samples_leaf, max_features=True, rng=self.rng)

    def _Bootstrap(self, X, y):
        idxs = self.rng.choice(len(X), size=len(X), replace=True)
        return X[idxs], y[idxs]

    def predict_proba(self, X_test):
        all_probas = np.zeros((len(self.trees), len(X_test)), dtype=np.float32)

        for i, tree in enumerate(self.trees):
            all_probas[i] = tree.predict_proba(X_test)

        return all_probas.mean(axis=0)

    def predict(self, X_test, threshold=0.5):
        probas = self.predict_proba(X_test)
        return (probas >= threshold).astype(int)