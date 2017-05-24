
# coding: utf-8

# In[1]:

# Take in list of elements and obtain Magpie elemental properties from Citrination
# Requires the elements.csv file from this GitHub repository
# Authorship: Chase Brisbois and Nicholas Wagner 
# Date: 2017-05-24
import numpy as np
import pandas as pd
from citrination_client import *
import time
client = CitrinationClient('API-KEY-HERE')


# In[2]:

elemental_data = pd.read_csv("../data/elements.csv")
element_names = elemental_data["Symbol letter"].loc[3:]


# In[78]:

def inquire(element):       
    input = {"Chemical formula": str(element)}
    resp = client.predict("27", input)
    element_prop_raw = resp['candidates'][0]
    element_prop = pd.DataFrame.from_dict(element_prop_raw)
    element_prop = element_prop[element_prop['Chemical formula'] != 0]
    for column in list(element_prop):
        if 'dop' in column:
            element_prop = element_prop.drop(column, axis=1)
        element_prop = element_prop.rename(index=str, columns={column: column.strip('_l1')})
    return element_prop


# In[79]:

df = pd.DataFrame()
for name in element_names[:]:
    if name == 'Lw':
        continue
    row = inquire(name)
    df = df.append(row)
df = df.rename(index=str, columns={"Chemical formula": "Symbol letter"})


# In[80]:

new_df = pd.merge(elemental_data, df, on='Symbol letter')


# In[81]:

new_df.to_csv('../data/Elements_gperiodic+magpie.csv')

