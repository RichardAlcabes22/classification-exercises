import acquire as acq
from env import uname, pwd, host
import pandas as pd
import os
from sklearn.model_selection import train_test_split

def prep_iris(df):
    '''
    prep iris will take in a single pandas dataframe
    and drop columns: species_id and measurement_id
    and rename species_name to species
    and aaddress NULLS
    and encoding cats
    '''
 
    df = df.drop(columns=['species_id','measurement_id'])
    df = df.rename(columns={'species_name':'species'},inplace=True)
    df = pd.concat([df,pd.get_dummies(df['species'],drop_first=True)],axis=1)
    return df

def prep_titanic(df):
    '''
    Accepts a df and drops unneeded columns, imputes missing values, and encodes cats
    '''
    #drop out any redundant, excessively empty, or bad columns
    df = df.drop(columns=['passenger_id','embarked','deck','class'])
    # impute average age and most common embark_town:
    df['age'] = df['age'].fillna(df.age.mean())
    df['embark_town'] = df['embark_town'].fillna('Southampton')
    # encode categorical values:
    df = pd.concat(
    [df, pd.get_dummies(df[['sex', 'embark_town']],
                        drop_first=True)], axis=1)
    return df

def prep_telco(df):
    '''
    Accepts a df and drops unneeded columns, imputes missing values, and encodes cats
    '''
    
    #drop out any redundant, excessively empty, or bad columns
    df = df.drop(columns=['Unnamed: 0','payment_type_id','internet_service_type_id','contract_type_id'])

    # encode categorical values:
    df = pd.concat(
    [df, pd.get_dummies(df[['gender', 'senior_citizen','partner','dependents','tech_support','streaming_tv',
                           'streaming_movies','paperless_billing','churn','contract_type',
                            'internet_service_type','payment_type']],
                        drop_first=True)], axis=1)
    return df

def split_data(df, target):
    '''
    split_data will split data into train,val,test based on 
    the values present in a cleaned version of df.  By default, data will be stratified
    by the target label
    
    '''
    train_val, test = train_test_split(df,train_size=0.8,random_state=2013,
                                   stratify=df[target])
    train, validate = train_test_split(train_val,train_size=0.7,random_state=2013,
                                   stratify=train_val[target])
    return train, validate, test