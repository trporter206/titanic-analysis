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
for dataset in [titanic_data]:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

title_table = pd.crosstab(titanic_data['Title'], titanic_data['Sex'])
# print title_table

for dataset in [titanic_data]:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
# print titanic_data[['Title', 'Survived']].groupby(['Title'], as_index=False).mean().sort_values(by='Survived', ascending=False)

title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in [titanic_data]:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

titanic_data = titanic_data.drop(['Name', 'PassengerId'], axis=1)

#convert categorical features to numeric for algo ease--------------------------
for dataset in [titanic_data]:
    dataset['Sex'] = dataset['Sex'].map({'female': 1, 'male': 0}).astype(int)

#fill in missing/null values. Guess Age values using median values for Age across sets of Pclass and Gender feature combinations--------------------------------------------------------------------
hist = sns.FacetGrid(titanic_data, row='Pclass', col='Sex')
hist.map(plt.hist, 'Age', alpha=.5, bins=20)
hist.add_legend()
# plt.show()

guess_ages = np.zeros((2,3))

for dataset in [titanic_data]:
    for i in range(0,2):
        for j in range(0,3):
            guess_df = dataset[(dataset['Sex'] == i) & (dataset['Pclass'] == j+1)]['Age'].dropna()

            age_guess = guess_df.median()

            #convert random age float to nearest .5 age
            guess_ages[i,j] = int(age_guess/0.5 + 0.5) * 0.5

    for i in range(0,2):
        for j in range(0,3):
            dataset.loc[ (dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1), 'Age'] = guess_ages[i,j]

    dataset['Age'] = dataset['Age'].astype(int)

#create 5 age bands for ease----------------------------------------------------
titanic_data['AgeBand'] = pd.cut(titanic_data['Age'], 5)
ageband_survival = titanic_data[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)

for dataset in [titanic_data]:
    dataset.loc[dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[dataset['Age'] > 64, 'Age']

titanic_data = titanic_data.drop(['AgeBand'], axis=1)

#create familysize combining parch and sibs-------------------------------------
for dataset in [titanic_data]:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1

family_survival = titanic_data[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# print family_survival

for dataset in [titanic_data]:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

alone_survival = titanic_data[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()
# print alone_survival

titanic_data = titanic_data.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
# print titanic_data.head()

#combine pclass and age---------------------------------------------------------
for dataset in [titanic_data]:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass
# print titanic_data.loc[:, ['Age*Class', 'Age', 'Pclass']].head(10)

#fill missing class values------------------------------------------------------
freq_port = titanic_data.Embarked.dropna().mode()[0]

for dataset in [titanic_data]:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)

embarked_survival = dataset[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean()
# print embarked_survival

for dataset in [titanic_data]:
    dataset['Embarked'] = dataset['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
# print titanic_data.head()

#fill single missing fare value-------------------------------------------------
titanic_data['Fare'].fillna(titanic_data['Fare'].dropna().median(), inplace=True)

#create fareband and set fare to ordinal values based on band-------------------
titanic_data['FareBand'] = pd.qcut(titanic_data['Fare'], 4)
fare_survival = titanic_data[['FareBand', 'Survived']].groupby(['FareBand'], as_index=False).mean().sort_values(by='FareBand', ascending=True)
# print fare_survival

for dataset in [titanic_data]:
    dataset.loc[dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare'] = 2
    dataset.loc[dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

titanic_data = titanic_data.drop(['FareBand'], axis=1)

print titanic_data.head(10)
