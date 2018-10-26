import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

titanic_data = pd.read_csv("titanic_data.csv")

#quick data overview------------------------------------------------------------
def overview(data):
    print('column names')
    print data.columns.values
    print('_'*40)
    print('column info')
    print data.info()
    print('_'*40)
    print('numeric columns')
    print data.describe()
    print('_'*40)
    print('non numeric columns')
    print data.describe(include=[np.object])

# overview(titanic_data)

#compare plcass, sex, sibsp, parch to survival rate-----------------------------
def pivot(v1, v2):
    pivot_table = titanic_data[[v1, v2]].groupby([v1], as_index=False).mean().sort_values(by=v2, ascending=False)
    print('_'*40)
    print pivot_table

pivot('Pclass', 'Survived')
pivot('Sex','Survived')
pivot('SibSp','Survived')
pivot('Parch','Survived')

#visual analysis of age and class survival--------------------------------------
g = sns.FacetGrid(titanic_data, col='Survived')
g.map(plt.hist, 'Age', bins=20)

grid = sns.FacetGrid(titanic_data, col='Survived', row='Pclass')
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend
# plt.show()
