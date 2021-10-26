import numpy as np
import pandas as pd
import warnings
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import recall_score, precision_score, make_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from baseline import Baseline
from ensemble_model import Ensemble


warnings.filterwarnings("ignore")

models = [Baseline(), LogisticRegression(), RandomForestClassifier(), GradientBoostingClassifier(), KNeighborsClassifier(), GaussianNB(), BernoulliNB()]
models_to_save = [RandomForestClassifier(), GradientBoostingClassifier()]


def pprint(model_scores):
    for model in model_scores:
        avg = np.mean(model_scores[model])
        big = np.max(model_scores[model])
        print(str(model).ljust(30) + str(round(avg, 2)) + ' +- ' + str(round(big-avg, 4)))



def save_model(model):
    with open(f'models/{str(model).split("(")[0].lower()}_model.pickle', 'wb') as f:
        pickle.dump(model, f)
        f.close()
    cont = input(f"Saved {model} to pickle, continue? [y][n]\n")
    if cont == 'n':
        exit()
    return
    


def run_gridsearch(model, X_train, y_train):
    if type(model) == RandomForestClassifier:
        model = RandomForestClassifier(max_depth = 50).fit(X_train, y_train)
    elif type(model) == GradientBoostingClassifier: 
        model = GradientBoostingClassifier(max_depth = 4, learning_rate = .25).fit(X_train, y_train)
    return model


def test_model(model, data, save_models, models_to_save):
    model_copy = model
    models_to_save = [str(model) for model in models_to_save]
    
    df = data.copy()
    X = data.drop('fraud', axis=1).values
    y = data.pop('fraud').values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    if type(model) == RandomForestClassifier or type(model) == GradientBoostingClassifier:
        model = run_gridsearch(model, X_train, y_train)
    else:
        model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    recall = recall_score(y_test, y_hat)
    precision = precision_score(y_test, y_hat)
    if save_models and str(model_copy) in models_to_save:
        save_model(model)
    print(f'{model} precision: {precision}')
    print(f'{model} recall: {recall}')
    return recall * .7 + precision * .3, df


def run_all_models(filename="fraud_feature_4", iters=1, models = models, save_models = False, models_to_save = []):
    df = pd.read_csv(f'data/{filename}.csv')
    df.drop(df.columns.values[0], axis=1, inplace=True)
    for i in range(iters):
        model_scores = {}
        for model in models:
            print(f'Running {model}')
            our_score, df = test_model(model, df, save_models, models_to_save)
            print(f'{model} scored {our_score}\n')
            if model in model_scores:
                model_scores[model].append(our_score)
            else:
                model_scores[model] = [our_score]
    if iters > 10:
        pprint(model_scores)


if __name__ == '__main__':
    run_all_models(save_models = False)



class LiveData:

    def get_data(self):
        '''
        gets live data

        self.live_data = APIClient.get_data()
        data_guess_dict = {}
        for row in live data:
            row = clean row
            guess = self.guess(row)
            data_guess_dict[guess].append(row)
        return data_guess_dict

        '''
        pass
    
    def guess(self, row):
        '''
        predicts fraud or not fraud based on a row
        model = open pickle file
        return model.predict(row)
        '''
        pass
    

    def update_postgres(self, data):
        '''
        updates postgres with self.live_data
        '''
        pass

'''
open postgres, use that for inital fill of html
while True:
    updater = LiveData()
    data_guess_dict = updater.get_data()
    update html
    updater.update_postgres()

'''