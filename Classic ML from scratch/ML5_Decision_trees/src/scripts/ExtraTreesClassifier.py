from scripts.DecisionTreeClassifier import *
from scripts.RandomForestClassifier import *

class ExtraTreeClassifier(MyDecisionTreeClassifier):
    
    def Best_split_feature(self, idxs, j, n, n_pos, old_impurity):
        x = self.X[idxs, j]

        if x.min() == x.max():
            return None, -1

        best_gain = -1
        best_t = None

        for _ in range(5):
            t = self.rng.uniform(x.min(), x.max())

            left_mask = x <= t
            # right_mask = ~left_mask

            left_n = left_mask.sum()
            right_n = n - left_n

            if left_n < self.min_samples_leaf or right_n < self.min_samples_leaf:
                continue

            left_pos = self.y[idxs][left_mask].sum()
            right_pos = n_pos - left_pos

            left_impurity = self.impurity_from_stats(left_n, left_pos)
            right_impurity = self.impurity_from_stats(right_n, right_pos)

            gain = n * old_impurity - left_n * left_impurity - right_n * right_impurity

            if gain > best_gain:
                best_gain = gain
                best_t = t

        if best_t is None:
            return None, -1

        return best_t, best_gain
    
class ExtraTreesClassifier(MyRandomForestClassifier):
    def _maketree(self):
        return ExtraTreeClassifier(self.max_depth, self.min_samples_split, self.min_samples_leaf, max_features=True, rng=self.rng)