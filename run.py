import time
import pandas as pd
import numpy as np
import psycopg2 as pg2
import lh_pipeline as pipe
import requests
import pickle


class LiveData():

    def __init__(self, model_path = 'models/randomforestclassifier_model.pickle'):
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        self.cursor = None
        self.db_conn = None

    def _connect_to_db(self):
        self.db_conn = pg2.connect(dbname='live_data', user='postgres',password='galvanize',host='localhost', port='5432')
        self.cursor = self.db_conn.cursor()
        if self.cursor:
            print('Connected to database')

    def _query_db(self):
        query = '''SELECT * FROM test'''
        self.cursor.execute(query)
        results = list(self.cursor)
        print(results)

    def get_data(self):
        self.live_data = EventAPIClient().get_data()
        data_guess_dict = {}  #fraud/not fraud keys, list of data for values

        test_df = pd.DataFrame(self.live_data)
        #print(f'Printing test dataframe...:\n:{test_df}')
        for idx,row in test_df.iterrows():
            # Clean and transform data prior to model use
            cleaned_row = pipe.read_live_data(row)
            #print(len(cleaned_row))
            # Make prediction on data
            guess, guess_prob, guess_conf = self.guess(cleaned_row)
            print(guess, guess_prob, guess_conf)
            self.update_database(row, guess)
            #data_guess_dict[guess] = cleaned_row

        #return data_guess_dict
        return cleaned_row

    def guess(self, row):
        prob = self.model.predict_proba(row.values.reshape(1,-1))
        #print(prob)
        if prob[0,1] < 0.35:
            confidence = 'low'
        elif prob[0,1] < 0.7:
            confidence = 'medium'
        else:
            confidence = 'high'

        return self.model.predict(row.values.reshape(1,-1)), prob, confidence

    def update_database(self, data_sample, predict):
        self._connect_to_db()
        #query = '''SELECT * FROM test'''
        #query = '''INSERT INTO test (text)
                   #VALUES ('World Again')'''
        #self.cursor.execute(query)
        #self.db_conn.commit()
        #self._query_db()
        columns = list(data_sample.index)
        table_name = 'test'
        values_str = []
        sql_string = "INSERT INTO %s (%s)\nVALUES %s" % (table_name,
                                                        ', '.join(columns),
                                                        values_str)
        print(sql_string)
        self.db_conn.close()
        

class EventAPIClient:
    """Realtime Events API Client"""
    
    def __init__(self, first_sequence_number=0,
                 api_url = 'https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key = 'vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db = None):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        
    def save_to_database(self, row):
        """Save a data row to the database."""
        print("Received data:\n" + repr(row) + "\n")  # replace this with your code

    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']
    
    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        requests_=[]
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                for row in data:
                    self.save_to_database(row)
                requests_.append(data)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)
        return requests_

if __name__ == '__main__':

    test_row = LiveData().get_data()


