from scripts.reqs import np


class MyDecisionTreeRegressor:

    def __init__(
        self,
        max_depth=7,
        min_samples_split=50,
        min_samples_leaf=10,
        n_bins=None,
        max_features= None,
        rng = 42
        ):
        
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.n_bins = n_bins

        self.max_features = max_features
        self.rng = rng

        self.root = None
        self.bin_edges = None


    def fit(self, X, y):
        self.X = np.array(X, dtype=np.float32)
        self.y = np.array(y, dtype=np.float32)

        if self.n_bins is not None:
            self.X = self.Make_bins(self.X)

        root_idxs = np.arange(len(self.X), dtype=np.int32)
        root_n = len(root_idxs)
        root_sum = self.y[root_idxs].sum()
        root_sum2 = (self.y[root_idxs] ** 2).sum()

        self.root = self.Node()
        stack = [(self.root, root_idxs, 0, root_n, root_sum, root_sum2)]

        while stack:
            node, idxs, depth, n, sum_y, sum_y2 = stack.pop()

            if self.Stop(depth, n, sum_y, sum_y2):
                self.Make_leaf(node, n, sum_y, sum_y2)
                continue

            split = self.Search_best_split(idxs, n, sum_y, sum_y2)
            if split is None:
                self.Make_leaf(node, n, sum_y, sum_y2)
                continue

            j, t, left_idxs, right_idxs = split

            left_n = len(left_idxs)
            right_n = len(right_idxs)

            left_sum = self.y[left_idxs].sum()
            right_sum = sum_y - left_sum

            left_sum2 = (self.y[left_idxs] ** 2).sum()
            right_sum2 = sum_y2 - left_sum2

            node.j = j
            node.t = t
            node.n_samples = n
            node.sum_y = sum_y
            node.sum_y2 = sum_y2
            node.left = self.Node()
            node.right = self.Node()

            stack.append((node.right, right_idxs, depth + 1, right_n, right_sum, right_sum2))
            stack.append((node.left, left_idxs, depth + 1, left_n, left_sum, left_sum2))

        return self

    def Search_best_split(self, idxs, n, sum_y, sum_y2):
        best_gain = 0.0
        best_j = None
        best_t = None

        old_impurity = self.impurity_from_stats(n, sum_y, sum_y2)

        p = self.X.shape[1]
        if self.max_features:
            m = max(1, int(np.sqrt(p)))
            features = self.rng.choice(p, size=m, replace=False)
        else:
            features = np.arange(p)

        for j in features:
            t, gain = self.Best_split_feature(idxs, j, n, sum_y, sum_y2, old_impurity)

            if t is not None and gain > best_gain:
                best_gain = gain
                best_j = j
                best_t = t

        if best_j is None or best_gain <= 0:
            return None

        col = self.X[idxs, best_j]
        left_mask = col <= best_t
        right_mask = ~left_mask

        left_idxs = idxs[left_mask]
        right_idxs = idxs[right_mask]

        return best_j, best_t, left_idxs, right_idxs

    def Best_split_feature(self, idxs, j, n, sum_y, sum_y2, old_impurity):
        x = self.X[idxs, j]

        if x.min() == x.max():
            return None, -1

        order = np.argsort(x)
        x_sorted = x[order]
        y_sorted = self.y[idxs][order]

        left_n = 0
        left_sum = 0.0
        left_sum2 = 0.0

        best_gain = 0.0
        best_t = None

        for i in range(n - 1):
            left_n += 1
            left_sum += y_sorted[i]
            left_sum2 += y_sorted[i] ** 2

            right_n = n - left_n
            right_sum = sum_y - left_sum
            right_sum2 = sum_y2 - left_sum2

            if left_n < self.min_samples_leaf or right_n < self.min_samples_leaf:
                continue

            if x_sorted[i] == x_sorted[i + 1]:
                continue

            left_impurity = self.impurity_from_stats(left_n, left_sum, left_sum2)
            right_impurity = self.impurity_from_stats(right_n, right_sum, right_sum2)

            gain = n * old_impurity - left_n * left_impurity - right_n * right_impurity

            if gain > best_gain:
                best_gain = gain
                best_t = (x_sorted[i] + x_sorted[i + 1]) / 2

        return best_t, best_gain

    def impurity_from_stats(self, n, sum_y, sum_y2):
        if n == 0:
            return 0.0
        return sum_y2 / n - (sum_y / n) ** 2

    def Stop(self, depth, n, sum_y, sum_y2):
        if depth >= self.max_depth:
            return True
        if n < self.min_samples_split:
            return True
        if self.impurity_from_stats(n, sum_y, sum_y2) == 0:
            return True
        return False

    def Make_leaf(self, node, n, sum_y, sum_y2):
        node.answer = self.Answer(n, sum_y)
        node.n_samples = n
        node.sum_y = sum_y
        node.sum_y2 = sum_y2

    def Answer(self, n, sum_y):
        return sum_y / n

    def Traverse(self, X, Node):
        if Node.answer is not None:
            return Node.answer

        if X[Node.j] <= Node.t:
            return self.Traverse(X, Node.left)
        else:
            return self.Traverse(X, Node.right)

    def predict(self, X_test):
        X = self.Apply_bins(X_test)
        preds = np.zeros(len(X), dtype=np.float32)

        for i in range(len(X)):
            preds[i] = self.Traverse(X[i], self.root)

        return preds
    
    def Make_bins(self, X):
        X_binned = np.empty_like(X, dtype=np.float32)
        self.bin_edges = []

        for j in range(X.shape[1]):
            col = X[:, j]

            if self.n_bins is None:
                self.bin_edges.append(None)
                X_binned[:, j] = col
                continue

            qs = np.linspace(0, 1, self.n_bins + 1)[1:-1]
            edges = np.quantile(col, qs)
            edges = np.unique(edges)

            if len(edges) == 0:
                self.bin_edges.append(None)
                X_binned[:, j] = col
            else:
                self.bin_edges.append(edges)
                X_binned[:, j] = np.digitize(col, edges).astype(np.float32)

        return X_binned

    def Apply_bins(self, X):
        X = np.array(X, dtype=np.float32)

        if self.bin_edges is None:
            return X

        X_binned = np.empty_like(X, dtype=np.float32)

        for j in range(X.shape[1]):
            edges = self.bin_edges[j]
            if edges is None:
                X_binned[:, j] = X[:, j]
            else:
                X_binned[:, j] = np.digitize(X[:, j], edges).astype(np.float32)

        return X_binned


    class Node:
        def __init__(
            self,
            j=None,
            t=None,
            left=None,
            right=None,
            answer=None,
            n_samples=None,
            sum_y=None,
            sum_y2=None
        ):
            self.j = j
            self.t = t
            self.left = left
            self.right = right
            self.answer = answer
            self.n_samples = n_samples
            self.sum_y = sum_y
            self.sum_y2 = sum_y2