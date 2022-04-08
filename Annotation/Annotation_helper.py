import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from textdistance import levenshtein
from IPython.display import display, HTML
from IPython.display import clear_output
import time
import math

def preprocess(df):
    return df.dropna(how='all', axis=1).replace('[Leeg]', np.nan).replace('[leeg]', np.nan).replace('[…]', np.nan).replace('[...]', np.nan).dropna(how='all', axis=0)

def preprocess_column(col):
    return col.str.lower()

def preprocess_columns(df):
    for col in df.columns:
        preprocess_column(df[col])
        
def drop_missing(df, cols):
    df2 = df.copy()
    for col in cols:
        df2 = df2[df2[col].isnull()]
    return pd.concat([df,df2]).drop_duplicates(keep=False)

def load_transactions(path):
    transactions = preprocess(pd.read_csv(path))
    transactions = drop_missing(transactions, ["SlaafNaamNieuw", "KoperVoornaam", "KoperAchternaam"])
    transactions = transactions.drop(columns=["Verkoop", "Inventarisnummer", "Scan", "Plaats"])
    return transactions

def load_permissions(path):
    permissions = preprocess(pd.read_csv(path))
    permissions = drop_missing(permissions, ["SlaafNaamNieuw", "BezitterVoornaam", "BezitterAchternaam"])
    return permissions

def fuzzy_search(df, query, col_name):
    col = df[col_name].to_numpy()
    res = np.zeros(len(col))
    for i, val in enumerate(col):
        if type(val) == str and type(query[0]) == str:
            r = fuzz.ratio(val, query[0])
        elif type(val) != str and type(query[0]) != str:
            r = 70
        else:
            r = 70
        res[i]= r * query[1]
    df[f"{col_name}_dist"] = res
    return df , f"{col_name}_dist"

def fuzzy_match(df, query):
    df = df.copy()
    dist_col_names = []
    df["total_dist"] = 0
    for key in query.keys():
        df, col_name = fuzzy_search(df, query[key], key)
        dist_col_names.append(col_name)
        df["total_dist"] = df["total_dist"] + df[col_name]
    return df.sort_values(by=['total_dist'], ascending=False)

def generate_query(s, translation):
    res = dict()
    for key in s.keys():
        try:
            res[translation[key][0]] = (s[key], translation[key][1])
        except:
            pass
    return res

def get_n_dict_value(d, n=0):
    d2 = dict()
    for key in d.keys():
        d2[key] = d[key][0]
    return d2

def read_or_make_csv(path, col_names=["Annotator", "transaction_indx", "permission_indx"]):
    try:
        df = pd.read_csv(path)
    except:
        df = pd.DataFrame(columns=col_names)
    return df

def Annotate_data(df1, df2, translation, output_file, Annotator_name="Bas"):
    output = read_or_make_csv(output_file)
    for i, row in enumerate(df1):
        df1_row = df1.iloc[i]
        q = generate_query(df1_row, translation)
        m = fuzzy_match(df2, q)
        print("Query: ", get_n_dict_value(q))
        display(HTML(pd.DataFrame.from_dict(get_n_dict_value(q)).to_html()))
        print("Possible matches: ")
        display(HTML(m[get_n_dict_value(translation).values()].head(n=12).to_html()))
        res = input("Index of most likely match: ").split(" ")
        res_id = []
        if res != ['']:
            for el in res:
                res_id = df2.loc[int(el)]["ID"]
                res_df = pd.DataFrame(data={"Annotator":Annotator_name,"transaction_indx":res_id,"permission_indx":df1_row["ID"]})
                output = pd.concat([output, res_df]).reset_index(drop=True)
            output.to_csv(output_file)






