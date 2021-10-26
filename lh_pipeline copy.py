import pandas as pd

def get_avg_price(x):
    total_cost = 0
    total_qua = 0
    for d in x:
        total_cost += (d['cost'] * d['quantity_total'])
        total_qua += d['quantity_total']
    if total_qua == 0:
        return 0
    return total_cost / total_qua

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
    new_df = df[['user_age', 'num_payouts', 'num_order', 'has_analytics', 'has_logo', 'name_length', 'sale_duration2', 'show_map', 'fraud']]
    new_df[['past_payouts', 'total_payout_amt']] = (df['previous_payouts'].apply(tot_money).tolist())
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

