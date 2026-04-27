from scripts.reqs import *
from scripts.reqs import np


class MyDecisionTreeClassifier:

    def __init__(self, max_depth = 7, min_samples_split = 50, min_samples_leaf = 10, weight_balanced = True):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None

    def fit(self, X, y):
        self.X, self.y = np.array(X), np.array(y)
        self.root = self.build(np.arange(len(X)), 0)

    def build(self, idxs, depth):
        if self.Stop(idxs, depth):
            return self.Node(answer=self.Answer(idxs))
        split = self.Search_best_split(idxs)
        if not split:
            return self.Node(answer=self.Answer(idxs))
        j, t, left, right = split
        node = self.Node(j, t, self.build(left, depth+1), self.build(right, depth+1))
        return node

    def Search_best_split(self, m_idxs):
        max_gain = 0
        optimal_border = None
        X_m = self.X[m_idxs]

        p = self.X.shape[1]

        if self.max_features:
            m = max(1, int(np.sqrt(p)))
            features = self.rng.choice(p, size=m, replace=False)
        else:
            features = np.arange(p)

        for j in features:

            values = np.unique(X_m[:, j])

            if len(values) < 2:
                continue
            thresholds = (values[:-1] + values[1:]) / 2

            for t in thresholds:
                gain = self.calc_gain(m_idxs, j, t)
                if gain > max_gain:
                    max_gain, optimal_border = gain, (j, t)

        if optimal_border is None:
            return None

        j, t = optimal_border
        left_idx = m_idxs[X_m[:, j] <= t]
        right_idx = m_idxs[X_m[:, j] > t]

        return j, t, left_idx, right_idx

    def calc_gain(self, m_idxs, j, t):

        X_m = self.X[m_idxs]
        l_idx = m_idxs[X_m[:, j] <= t]
        r_idx = m_idxs[X_m[:, j] > t]

        if len(l_idx) < self.min_samples_leaf or len(r_idx) < self.min_samples_leaf:
            return -1
        else:
            old = self.impurity(m_idxs)
            left = self.impurity(l_idx)
            right = self.impurity(r_idx)

            n_o, n_l, n_r = len(m_idxs), len(l_idx), len(r_idx)
            return n_o * old - n_l * left - n_r * right

    def impurity(self, m_idxs): 
        p = (self.y[m_idxs] == 1).sum()/len(self.y[m_idxs])
        return 2*p*(1-p)

    def Stop(self, idxs, depth):

        if self.max_depth == depth or len(idxs) < self.min_samples_split:
            return True
        else: 
            return False

    def Answer(self, idxs):
        return self.y[idxs].mean()

    def Traverse(self, X, Node):
        
        if Node is None:
            return
        if Node.answer is not None:
            return Node.answer
        

        if X[Node.j] <= Node.t:
            return self.Traverse(X, Node.left)
        else:
            return self.Traverse(X, Node.right)

    def Predict_proba(self, X_test):
        X = np.array(X_test)
        preds = np.zeros(len(X_test))
        for i in range(len(X)):
            preds[i] = self.Traverse(X[i], self.root)
        return preds


    class Node:
        def __init__(self, j = None, t = None, left = None, right = None, answer = None):
            self.t, self.j = t, j
            self.left = left
            self.right, self.answer = right, answer