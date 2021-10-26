import numpy as np

class Baseline:

    def __repr__(self):
        return "Baseline()"

    def fit(self, X, y):
        unique, counts = np.unique(y, return_counts = True)
        counts = [i/sum(counts) for i in counts]
        self.proportions = dict(zip(unique, counts))
    
    def predict(self, X):
        ret_arr = np.zeros(shape=(X.shape[0], 1))
        for i in range(X.shape[0]):
            ret_arr[i, 0] = np.random.choice(list(self.proportions.keys()), p = list(self.proportions.values()))
        return ret_arr


