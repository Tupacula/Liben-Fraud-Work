from sklearn.dummy import DummyClassifier
import pandas as pd

import pickle




if __name__ == '__main__':
    df = pd.read_json('data.zip')
    df['fraud'] = df['acct_type'].apply(lambda x: True if 'fraud' in x else False)
    X = df['venue_state']
    y = df['fraud']
    model = DummyClassifier(strategy='stratified')
    model.fit(X, y)
    with open('dummy_model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)
    

