import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as pyplot

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

#compare class to survival rate. groupby is like pivot in excel-----------------
class_survival = titanic_data[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)

# print class_survival

#compare sex and survival rate--------------------------------------------------
sex_survival = titanic_data[['Sex', 'Survived']].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)

# print sex_survival

#compare number of siblings to survival rate------------------------------------
sibling_count_survival = titanic_data[['SibSp', 'Survived']].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)

# print sibling_count_survival

#compare number of accompanying parents/children with survival------------------
with_parent_or_child_survival = titanic_data[['Parch', 'Survived']].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)

# print with_parent_or_child_survival
