# inside acquire.py script:
from env import uname, pwd, host
import pandas as pd
import os
from sklearn.model_selection import train_test_split

def get_sql_url(db, u=uname, p=pwd, h=host):
    '''
    get_sql_url will pull the credentials present from any current env
    file in the same directory as this acquire script
    and will return a connection based on what schema as handed to the 
    function call
    '''
    return f'mysql+pymysql://{u}:{p}@{h}/{db}'

#-----------------------------------------------------------

def acquire_employee_head(schema, u=uname, p=pwd, h=host):
    '''
    acquire_employee_head will grab the first 20 rows
    of the employees table from the employees schema and return it
    as a pandas dataframe.
    
    note that this function is dependent on the schema being passed
    as employees due to the query being defined in the scope of the function
    '''
    query = 'SELECT * FROM employees LIMIT 20'
    url = get_sql_url(schema, u=u,p=p,h=h)
    return pd.read_sql(query,url)



def get_titanic_data(schema,u=uname,p=pwd,h=host):
    '''
    checks to see if .csv file exists as filename.csv
    returns titanic_db.passengers from codeup as a pandas DF
    '''
    filename = "titanic.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename,index_col=False)
    else:
        query = 'SELECT * FROM passengers'
        url = get_sql_url(schema,u=u, p=p, h=h)
        df = pd.read_sql(query, url)
        df.to_csv(filename,index=False)
        return df


def get_iris_data(schema,u=uname,p=pwd,h=host):
    '''
    returns iris_db data from codeup as a pandas DF
    '''
    filename = "iris.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename,index_col=False)
    else:
        query = 'SELECT * FROM measurements JOIN species USING(species_id)'
        url = get_sql_url(schema,u=u, p=p, h=h)
        df = pd.read_sql(query, url)
        df.to_csv(filename,index=False)
        return df

def get_telco_data(schema,u=uname,p=pwd,h=host):
    '''
    returns telco_db data from codeup as a pandas DF
    '''
    filename = "telco.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename,index_col=False)
    else:
        query = 'SELECT * FROM customers JOIN contract_types USING(contract_type_id) JOIN internet_service_types USING(internet_service_type_id) JOIN payment_types USING(payment_type_id)'
        url = get_sql_url(schema,u=u, p=p, h=h)
        df = pd.read_sql(query, url)
        df.to_csv(filename,index=False)
        return df

######### USE THIS FOR THE NEW TELCO DATASET!!!!
def new_telco_data():
    '''
    This function reads the telco data from the Codeup db into a df.
    '''
    filename = "telco_new.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename,index_col=False)
    else:
        sql_query = """
                select * from customers
                join contract_types using (contract_type_id)
                join internet_service_types using (internet_service_type_id)
                join payment_types using (payment_type_id)
                """
    
        # Read in DataFrame from Codeup db.
        df = pd.read_sql(sql_query, get_sql_url('telco_churn'))
        df.to_csv(filename,index=False)
        return df


#----------------------------------------------------


def get_sql_pull(schema,query,u=uname,p=pwd,h=host):
    '''
    returns the results of a mySQL query from a specified 
    codeup schema as a pandas DF
    '''
    filename = f'{schema}.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename,index_col=False)
    else:
        url = get_sql_url(schema,u=u, p=p, h=h)
        df = pd.read_sql(query, url)
        df.to_csv(filename,index=False)
        return df
    