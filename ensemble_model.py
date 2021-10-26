import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from statistics import mode


models = [LogisticRegression(), RandomForestClassifier(), GradientBoostingClassifier(), KNeighborsClassifier(), GaussianNB(), BernoulliNB()]


class Ensemble:

    def __repr__(self):
        return "Ensemble()"

    def fit(self, X_train, y_train, models=[RandomForestClassifier(), GradientBoostingClassifier()]):
        self.models = []
        for model in models:
            model.fit(X_train, y_train)
            self.models.append(model)

    def predict(self, X_test):
        actual_votes = []
        for row in X_test:
            votes = []
            for model in self.models:
                y_hat = model.predict(row.reshape(1, -1))
                votes.append(y_hat[0])
            actual_votes.append(mode(votes))
        return np.array(actual_votes).reshape(-1, 1)
            