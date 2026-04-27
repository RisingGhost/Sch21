from scripts.reqs import np


class MyDecisionTreeClassifier:

    def __init__(
        self,
        max_depth=7,
        min_samples_split=50,
        min_samples_leaf=10,
        n_bins=None,
        weight_balance = None,
        max_features = None,
        rng = 42
        ):
        
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.n_bins = n_bins
        self.weight_balance = weight_balance

        self.max_features = max_features
        self.rng = rng
        
        self.root = None
        self.bin_edges = None


    def fit(self, X, y):
        self.X = np.array(X, dtype=np.float32)
        self.y = np.array(y, dtype=np.uint8)

        if self.weight_balance:
            p = self.y.mean()
            self.w1 = 1 / (2 * p)
            self.w0 = 1 / (2 * (1 - p))
        else:
            self.w1 = 1.0
            self.w0 = 1.0

        if self.n_bins is not None:
            self.X = self.Make_bins(self.X)

        root_idxs = np.arange(len(self.X), dtype=np.int32)
        root_n = len(root_idxs)
        root_pos = int(self.y[root_idxs].sum())

        self.root = self.Node()
        stack = [(self.root, root_idxs, 0, root_n, root_pos)]

        while stack:
            node, idxs, depth, n, n_pos = stack.pop()

            if self.Stop(depth, n, n_pos):
                self.Make_leaf(node, n, n_pos)
                continue

            split = self.Search_best_split(idxs, n, n_pos)
            if split is None:
                self.Make_leaf(node, n, n_pos)
                continue

            j, t, left_idxs, right_idxs = split

            left_n = len(left_idxs)
            right_n = len(right_idxs)

            left_pos = int(self.y[left_idxs].sum())
            right_pos = n_pos - left_pos

            node.j = j
            node.t = t
            node.n_samples = n
            node.n_pos = n_pos
            node.left = self.Node()
            node.right = self.Node()

            stack.append((node.right, right_idxs, depth + 1, right_n, right_pos))
            stack.append((node.left, left_idxs, depth + 1, left_n, left_pos))

        return self

    def Search_best_split(self, idxs, n, n_pos):
        best_gain = 0.0
        best_j = None
        best_t = None

        old_impurity = self.impurity_from_stats(n, n_pos)

        p = self.X.shape[1]
        if self.max_features:
            m = max(1, int(np.sqrt(p)))
            features = self.rng.choice(p, size=m, replace=False)
        else:
            features = np.arange(p)

        for j in features:
            t, gain = self.Best_split_feature(idxs, j, n, n_pos, old_impurity)

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

    def Best_split_feature(self, idxs, j, n, n_pos, old_impurity):
        x = self.X[idxs, j]

        if x.min() == x.max():
            return None, -1

        order = np.argsort(x)
        x_sorted = x[order]
        y_sorted = self.y[idxs][order]

        left_n = 0
        left_pos = 0

        best_gain = 0.0
        best_t = None

        for i in range(n - 1):
            left_n += 1
            left_pos += int(y_sorted[i])

            right_n = n - left_n
            right_pos = n_pos - left_pos

            if left_n < self.min_samples_leaf or right_n < self.min_samples_leaf:
                continue

            if x_sorted[i] == x_sorted[i + 1]:
                continue

            left_impurity = self.impurity_from_stats(left_n, left_pos)
            right_impurity = self.impurity_from_stats(right_n, right_pos)

            gain = n * old_impurity - left_n * left_impurity - right_n * right_impurity

            if gain > best_gain:
                best_gain = gain
                best_t = (x_sorted[i] + x_sorted[i + 1]) / 2

        return best_t, best_gain

    def impurity_from_stats(self, n, n_pos):
        if n == 0:
            return 0.0
   
        pos_w = n_pos * self.w1
        neg_w = (n - n_pos) * self.w0
        total_w = pos_w + neg_w
        p = pos_w / total_w

        return 2 * p * (1 - p)

    def Stop(self, depth, n, n_pos):
        if depth >= self.max_depth:
            return True
        if n < self.min_samples_split:
            return True
        if n_pos == 0 or n_pos == n:
            return True
        return False

    def Make_leaf(self, node, n, n_pos):
        node.answer = self.Answer(n, n_pos)
        node.n_samples = n
        node.n_pos = n_pos

    def Answer(self, n, n_pos):
        return n_pos / n

    def Traverse(self, X, Node):
        if Node.answer is not None:
            return Node.answer

        if X[Node.j] <= Node.t:
            return self.Traverse(X, Node.left)
        else:
            return self.Traverse(X, Node.right)

    def predict_proba(self, X_test):
        X = self.Apply_bins(X_test)
        probas = np.zeros(len(X), dtype=np.float32)

        for i in range(len(X)):
            probas[i] = self.Traverse(X[i], self.root)

        return probas
    
    def predict(self, X_test, threshold = 0.5):
        probas = self.predict_proba(X_test)
        return (probas >= threshold).astype(int)
    
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
            n_pos=None
        ):
            self.j = j
            self.t = t
            self.left = left
            self.right = right
            self.answer = answer
            self.n_samples = n_samples
            self.n_pos = n_pos