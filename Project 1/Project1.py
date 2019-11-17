# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:53:35 2019

@author: kalya
"""
import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("election_train.csv")
data.head()
data.info()
data_a_wide = pd.pivot_table(data, index = ['Year', 'State','County','Office'], columns = 'Party',values = 'Votes',aggfunc = [np.sum]).reset_index()
print(data_a_wide.head())
data_a_wide.info()
demo = pd.read_csv("demographics_train.csv")
demo.head()
demo.info()
state_abbrev = pd.Series({

    'Alabama': 'AL',

    'Alaska': 'AK',

    'Arizona': 'AZ',

    'Arkansas': 'AR',

    'California': 'CA',

    'Colorado': 'CO',

    'Connecticut': 'CT',

    'Delaware': 'DE',

    'District of Columbia': 'DC',

    'Florida': 'FL',

    'Georgia': 'GA',

    'Hawaii': 'HI',

    'Idaho': 'ID',

    'Illinois': 'IL',

    'Indiana': 'IN',

    'Iowa': 'IA',

    'Kansas': 'KS',

    'Kentucky': 'KY',

    'Louisiana': 'LA',

    'Maine': 'ME',

    'Maryland': 'MD',

    'Massachusetts': 'MA',

    'Michigan': 'MI',

    'Minnesota': 'MN',

    'Mississippi': 'MS',

    'Missouri': 'MO',

    'Montana': 'MT',

    'Nebraska': 'NE',

    'Nevada': 'NV',

    'New Hampshire': 'NH',

    'New Jersey': 'NJ',

    'New Mexico': 'NM',

    'New York': 'NY',

    'North Carolina': 'NC',

    'North Dakota': 'ND',

    'Northern Mariana Islands':'MP',

    'Ohio': 'OH',

    'Oklahoma': 'OK',

    'Oregon': 'OR',

    'Palau': 'PW',

    'Pennsylvania': 'PA',

    'Puerto Rico': 'PR',

    'Rhode Island': 'RI',

    'South Carolina': 'SC',

    'South Dakota': 'SD',

    'Tennessee': 'TN',

    'Texas': 'TX',

    'Utah': 'UT',

    'Vermont': 'VT',

    'Virgin Islands': 'VI',

    'Virginia': 'VA',

    'Washington': 'WA',

    'West Virginia': 'WV',

    'Wisconsin': 'WI',

    'Wyoming': 'WY',

})
demo["State"] = demo["State"].map(state_abbrev)
demo.sort_values(by = ['State']).head()

data_a_wide['County'] = data_a_wide['County'].str.replace(' County', '')
data_a_wide['County'] = data_a_wide['County'].str.lower()

demo['County'] = demo['County'].str.lower()
# Merge dataset data_a_wide and dataset demo
data_merged = pd.merge(data_a_wide, demo, how = 'inner',
                       on = ['State','County'], sort = True)
print(data_merged.head())
data_merged.info()

#Task3
# There are 23 attributes in the merged dataset. 
# The attributes "(Year, )" and "(Office, )" are the irrelevant attributes. And the attributes "(State, )" and "(County, ) are redundant attributes"

#Task 4
data_merged.info()

#Task 4

#There are no missing values in the merged dataset. Check the above info.

#Task 5
data_merged['Party'] = (data_merged[("sum", "Democratic")] > data_merged[('sum','Republican')]).astype("int64")
data_merged.head()

#Task 6
democratic = data_merged["Total Population"][data_merged["Party"] == 1]
print(democratic.mean())
republic = data_merged["Total Population"][data_merged["Party"] == 0]
print(republic.mean())

# TASK 6

[stat, pvalue] = stats.ttest_ind(democratic, republic, equal_var = False)
print(round(stat,3))
print(pvalue*2)

#Task 6
# As pvalue is less than the given significance level = 0.05, 
# we can reject the null hypothesis that the population mean of democratic and republic counties are equal.

#Task 7
democratic_MHI = data_merged["Median Household Income"][data_merged["Party"] == 1]
print(democratic.mean())
republic_MHI = data_merged["Median Household Income"][data_merged["Party"] == 0]
print(republic.mean())

# TASK 7
[stat, pvalue] = stats.ttest_ind(democratic_MHI, republic_MHI, equal_var = False)
print(round(stat,3))
print(pvalue*2)

#Task 7
# As pvalue is less than the given significance level = 0.05, 
# we can reject the null hypothesis that the mean Median Household Income of democratic and republic counties are equal.



change_values = pd.Series({1 : "Demo", 0 : "Rep"})
data_merged["Party"] = data_merged["Party"].map(change_values)
data_merged.head()



fips =data_merged['FIPS']
values = data_merged['Party']

fig = ff.create_choropleth(fips=fips, values=values)
fig.layout.template = None
fig.show()

