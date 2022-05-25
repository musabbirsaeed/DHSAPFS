import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

st.write("# DHS APFS Weekly Update")

def get_data():
    old_link = "https://raw.githubusercontent.com/musabbirsaeed/DHSAPFS/main/Public_old.csv"
    old = pd.read_csv(old_link)
    new_link = "https://raw.githubusercontent.com/musabbirsaeed/DHSAPFS/main/Public_new.csv"
    new = pd.read_csv(new_link)

    return old, new

def clean_data():
    old, new = get_data()    
    old.NAICS = old.NAICS.apply(lambda x: x[:7])
    new.NAICS = new.NAICS.apply(lambda x: x[:7])
    search_terms = ['541611','541618','541690','541720','541990','541511','541512','541519','541612','611430', '54151S'] 
    LAMBDA_search_term = lambda x: any(a_search_term.lower() in x.lower() for a_search_term in search_terms)

    old = old[old['NAICS'].apply(LAMBDA_search_term)]
    new = new[new['NAICS'].apply(LAMBDA_search_term)]

    return old, new

def find_dif():
    old, new = clean_data()
    added = new[~new.apply(tuple,1).isin(old.apply(tuple,1))].reset_index(drop=True)
    dropped = old[~old.apply(tuple,1).isin(new.apply(tuple,1))].reset_index(drop=True)
    return added, dropped

added, dropped = find_dif()

st.write("Recently added")

AgGrid(added, enable_enterprise_modules = True, height = 800)

st.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

st.write("Recently dropped")

AgGrid(dropped, enable_enterprise_modules = True, height = 800)
