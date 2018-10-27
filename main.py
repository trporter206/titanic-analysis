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

#func to compare variables. v2 must be numeric----------------------------------
def pivot(v1, v2):
    pivot_table = titanic_data[[v1, v2]].groupby([v1], as_index=False).mean().sort_values(by=v2, ascending=False)
    print('_'*40)
    print pivot_table

# pivot('Pclass', 'Survived')
# pivot('Sex','Survived')
# pivot('SibSp','Survived')
# pivot('Parch','Survived')

#visual analysis of age and class survival--------------------------------------
g = sns.FacetGrid(titanic_data, col='Survived')
g.map(plt.hist, 'Age', bins=20)

grid = sns.FacetGrid(titanic_data, col='Survived', row='Pclass')
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend

plot = sns.FacetGrid(titanic_data, row='Embarked')
plot.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
plot.add_legend()

bar = sns.FacetGrid(titanic_data, row='Embarked', col='Survived')
bar.map(sns.barplot, 'Sex', 'Fare', alpha=.5, ci=None)
bar.add_legend()

# plt.show()

#start dropping unnecessary features for determining survival-------------------
titanic_data = titanic_data.drop(['Ticket', 'Cabin'], axis=1)

#create new feature for title of passenger--------------------------------------
data = [titanic_data]
for dataset in data:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

title_table = pd.crosstab(titanic_data['Title'], titanic_data['Sex'])
# print title_table

for dataset in data:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')

# print titanic_data[['Title', 'Survived']].groupby(['Title'], as_index=False).mean().sort_values(by='Survived', ascending=False)

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in data:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

print titanic_data.head()
