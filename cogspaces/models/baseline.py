from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression


class MultiLogisticClassifier(BaseEstimator):
    def __init__(self, l2_penalty=1e-4, verbose=0, max_iter=1000):
        self.l2_penalty = l2_penalty
        self.verbose = verbose
        self.max_iter = max_iter

    def fit(self, X, y, callback=None):
        self.estimators_ = {}
        for study in X:
            n_samples = X[study].shape[0]
            C = 1. / (n_samples * self.l2_penalty)
            self.estimators_[study] = LogisticRegression(
                solver='lbfgs',
                multi_class='multinomial',
                C=C, max_iter=self.max_iter,
                tol=0,
                verbose=self.verbose).fit(X[study], y[study])

    def predict_proba(self, X):
        res = {}
        for study, this_X in X:
            res[study] = self.estimators_[study].predict_proba(this_X)
        return res

    def predict(self, X):
        res = {}
        for study, this_X in X.items():
            res[study] = self.estimators_[study].predict(this_X)
        return res