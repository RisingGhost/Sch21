# Карта построения дерева

## 1. Общий поток обучения

```text
fit(X, y)
│
├─ 1. приведение типов
│     self.X -> float32
│     self.y -> uint8
│
├─ 2. опционально биннинг
│     self.X = Make_bins(self.X)
│     self.bin_edges сохраняются в памяти
│
├─ 3. создание корня
│     root_idxs = [0, 1, 2, ..., n-1]
│     root_n = len(root_idxs)
│     root_pos = sum(y[root_idxs])
│     self.root = Node()
│
├─ 4. инициализация стека
│     stack = [(root_node, root_idxs, depth=0, n=root_n, n_pos=root_pos)]
│
└─ 5. цикл построения
      while stack:
          node, idxs, depth, n, n_pos = stack.pop()
          │
          ├─ Stop(depth, n, n_pos)
          │    │
          │    ├─ True  -> Make_leaf(node, n, n_pos)
          │    └─ False -> Search_best_split(idxs, n, n_pos)
          │
          └─ Search_best_split(...)
               │
               ├─ old_impurity = impurity_from_stats(n, n_pos)
               │
               ├─ цикл по признакам j
               │    │
               │    └─ Best_split_feature(idxs, j, n, n_pos, old_impurity)
               │         │
               │         ├─ x = self.X[idxs, j]
               │         ├─ если признак константный -> None
               │         ├─ order = np.argsort(x)
               │         ├─ x_sorted = x[order]
               │         ├─ y_sorted = self.y[idxs][order]
               │         │
               │         └─ один проход слева направо
               │              left_n, left_pos обновляются инкрементально
               │              right_n = n - left_n
               │              right_pos = n_pos - left_pos
               │
               │              проверки:
               │              - left_n >= min_samples_leaf
               │              - right_n >= min_samples_leaf
               │              - x_sorted[i] != x_sorted[i+1]
               │
               │              вычисления:
               │              - left_impurity = impurity_from_stats(left_n, left_pos)
               │              - right_impurity = impurity_from_stats(right_n, right_pos)
               │              - gain = n*old - left_n*left - right_n*right
               │
               │              если gain лучший:
               │              - сохранить best_gain
               │              - сохранить best_t = midpoint
               │
               ├─ выбрать лучший признак и лучший threshold среди всех j
               │
               ├─ если лучшего split нет или gain <= 0
               │    └─ return None
               │
               └─ если split найден
                    ├─ col = self.X[idxs, best_j]
                    ├─ left_mask = col <= best_t
                    ├─ right_mask = ~left_mask
                    ├─ left_idxs = idxs[left_mask]
                    ├─ right_idxs = idxs[right_mask]
                    └─ return best_j, best_t, left_idxs, right_idxs