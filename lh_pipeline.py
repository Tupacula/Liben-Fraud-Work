import pandas as pd
import numpy as np

test = pd.read_csv('data/fraud_feature_4.csv', index_col=0)


def get_avg_price(x):
    total_cost = 0
    total_qua = 0
    for d in x:
        total_cost += (d['cost'] * d['quantity_total'])
        total_qua += d['quantity_total']
    if total_qua == 0:
        return 0
    return total_cost / total_qua
def get_tickets(tickets):
    amt_sold = 0
    amt_tickets = 0
    for ticket in tickets:
        amt_tickets += ticket['quantity_total']
        amt_sold += ticket['quantity_sold']
    return amt_sold, amt_tickets

def tot_money(payouts):
    amount = len(payouts)
    money = 0
    if amount >0:
        for payout in payouts:
            money += payout['amount']
    return amount, money


def get_training_matrix(jsondf):
    df = pd.read_json(jsondf)
    df['fraud'] = df['acct_type'].apply(lambda x: True if 'fraud' in x else False)
    new_df = df[['user_age', 'has_analytics', 'fb_published', 'has_logo', 'name_length', 'show_map', 'fraud', 'body_length']]
    new_df[['past_payouts', 'total_payout_amt']] = (df['previous_payouts'].apply(tot_money).tolist())
    new_df[['amt_sold, amt_tickets']] = df['ticket_types'].apply(get_tickets)
    new_df['gmail'] = (df['email_domain'] == 'gmail.com')
    new_df['yahoo'] = (df['email_domain'] == 'yahoo.com')
    new_df['hotmail'] = (df['email_domain'] == 'hotmail.com')
    new_df['aol'] = (df['email_domain'] == 'aol.com')
    new_df['listed'] = df['listed'].apply(lambda x: 1 if x == 'y' else 0)
    df['sale_duration'][df['sale_duration'].isna()] = df['sale_duration2'][df['sale_duration'].isna()]
    new_df['sale_duration'] = df['sale_duration']
    payout_dummies = pd.get_dummies(df['payout_type'], drop_first=True)
    new_df[payout_dummies.columns] = payout_dummies
    user_dummies = pd.get_dummies(df['user_type'], drop_first=True)
    new_df[user_dummies.columns] = user_dummies
    df['country'].fillna('')
    country_dummies = pd.get_dummies(df['country'], drop_first=True)
    new_df[country_dummies.columns] = country_dummies
    new_df['avg_price']= df['ticket_types'].apply(get_avg_price)
    new_df['delivery_method'] = df['delivery_method']
    new_df.dropna(inplace=True)


    return new_df

def read_live_data(df):
    new_df = pd.Series(0, index=test.columns)
    new_df.drop('fraud', inplace=True)
    new_df[['user_age',  'has_analytics', 'has_logo', 'fb_published', 'name_length', 'show_map', 'body_length']] = \
    df[['user_age', 'has_analytics', 'has_logo', 'fb_published', 'name_length','show_map',  'body_length']]
    new_df[['past_payouts', 'total_payout_amt']] = tot_money(df['previous_payouts'])
    if df['listed'] == 'y':
        new_df['listed'] = 1
    else:
        new_df['listed'] = 0

    if np.isnan(df['sale_duration']):
        new_df['sale_duration'] = 0
    else:
        new_df['sale_duration'] = df['sale_duration']
    email = df['email_domain']
    if email in ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com']:
        new_df[email[:-4]] = 1
    user_type = str(df['user_type'])
    if user_type in new_df.index:
        new_df[user_type] = 1
    payout_type = df['payout_type']
    if payout_type in new_df.index:
        new_df[payout_type] = 1
    country = df['country']
    if country in new_df.index:
        new_df[country] = 1
    return new_df

    
    
    new_df['delivery_method'] = df['delivery_method']
    new_df['avg_price']= df['ticket_types'].apply(get_avg_price)


    
    