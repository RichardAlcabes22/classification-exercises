import matplotlib.pyplot as plt
import seaborn as sns
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
    df = df.rename(columns={'species_name':'species'})
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
    df = df.drop(columns=['payment_type_id','internet_service_type_id','contract_type_id'])

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
    the values present in a cleaned version of df.  Target parameter is intended to 
    take an argument that specifies the target variable and stratisfies the splits by the target.  
    However, data can be stratified by any column other than the target label if desired.
    
    '''
    train_val, test = train_test_split(df,train_size=0.8,random_state=2013,
                                   stratify=df[target])
    train, validate = train_test_split(train_val,train_size=0.7,random_state=2013,
                                   stratify=train_val[target])
    return train, validate, test


#------------------------------------------

def remind_data_prep():
    '''
    A quick function call to print out all possible data prep steps to inspect and execute should
    they be required
    '''
    print(f'-SUMMARIZE with head(),describe().T,info(),isnull(), isnull.sum().isnull.mean(),\n\
          value_counts(), .shape\n\
-PLOT with plt.hist(),plt.boxplot,plt.barchart(),plt.scatter\n\
-DOCUMENT takeaways and outline further cleaning steps to take\n\
-MISSINGNESS...OUTLIERS...DATA ERRORS...TEXT NORMALIZATION (caps vs.lowercase)\n\
-TIDYDATA...CALCULATED COLUMNS...RENAME COLUMNS...DROP COLUMNS\n\
-DATATYPES...SCALE NUMERIC DATA')
    

def cat_num_cols(df):
    cat_cols, num_cols = [], []
    for col in df.columns:
        if df[col].dtype == 'O':
            cat_cols.append(col)
        else:
            if df[col].nunique() < 6:
                cat_cols.append(col)
            else:
                num_cols.append(col)
    return cat_cols, num_cols

def ex_cat_cols(cat_cols,train_df):
    for col in cat_cols:
        print(f'Univariate assessment of feature {col}:')
        sns.countplot(data=train_df, x=col)
        plt.show()
        print(
        pd.concat([train_df[col].value_counts(),
        train_df[col].value_counts(normalize=True)],
                axis=1))