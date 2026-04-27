from scripts.reqs import np
from scripts.DecisionTreeRegressor import *

class GDBTClassifier:

    def __init__(self, lr= 0.01, number_of_trees=100, max_depth=7, min_samples_split=50, min_samples_leaf=10, max_features = True, n_bins = 64, random_state=42):
        self.lr = lr
        self.number_of_trees=number_of_trees
        self.max_depth=max_depth
        self.min_samples_split=min_samples_split
        self.min_samples_leaf=min_samples_leaf
        self.random_state=random_state
        self.rng = np.random.default_rng(random_state)
        self.max_features = max_features
        self.n_bins = n_bins

    def fit(self, X, y):
        self.X = np.array(X, dtype=np.float32)
        self.y = np.array(y, dtype=np.float32)
        self.trees = []
        

        self.y_base = self.logit(self.y.mean(axis=0))
        # self.y_base = self.logit(0.5)
        self.y_pred = np.full(len(self.y), self.y_base, dtype = np.float32)

        for _ in range(self.number_of_trees):
            grad = self.loss(self.y, self.y_pred)
            tree = MyDecisionTreeRegressor(self.max_depth, self.min_samples_split, self.min_samples_leaf, max_features=self.max_features, rng=self.rng, n_bins=self.n_bins)
            tree.fit(self.X, grad)

            self.trees.append(tree)
            self.y_pred += self.lr*tree.predict(self.X)



    def predict_proba(self, X_test):
        X = np.array(X_test, dtype = np.float32)
        pred = np.full(len(X), self.y_base, dtype = np.float32)

        for tree in self.trees:
            pred += self.lr * tree.predict(X) 
        return self.sigmoid(pred)
    
    def predict(self, X_test, threshold = 0.5):
        return (self.predict_proba(X_test) >= threshold).astype(np.uint8)
    
    def loss(self, y_true, y_pred):
        return y_true - self.sigmoid(y_pred)
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def logit(self, p):
        p = np.clip(p, 1e-15, 1 - 1e-15)
        return np.log(p / (1 - p))