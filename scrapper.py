# -*- coding: utf-8 -*-
"""scrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X_FAsFP64SRrpPjfW7Jnpl-9MeYpoCdN
"""

!pip install pmaw pandas

import pandas as pd
from pmaw import PushshiftAPI
api = PushshiftAPI()

import datetime as dt
before = int(dt.datetime(2022,10,10,0,0).timestamp())
after = int(dt.datetime(2018,4,1,0,0).timestamp())

subreddit="AskReddit"
limit=100000
posts=api.search_submissions(subreddit=subreddit, limit=limit, before=before, after=after)
print(f'Retrieved {len(posts)} posts from Pushshift')

comments_df = pd.DataFrame(posts)
comments_df.head(5)
#list(comments_df.columns)

list(comments_df.columns)

new_df=comments_df[['selftext', 'title', 'score', 'post_hint', 'created_utc', 'link_flair_text', 'pinned', 'total_awards_received', 'over_18', ]]

new_df.head(5)

comments_df.to_csv('df.csv', sep='\t')

import re
import pprint
import datetime
links=[]
titles=[]
scores=[]
ids=[]
data=[]
month=[]
flair=[]
img=[]
degree=[]
word_count=[]
domain = []
year = []


computerScience = [" computer science ", " cs ", " comp ", " ai ", " ml ", " networking ", " software ", " dl ", " graph ", " distributed ", " data science ", " ds ", " nlp ", " rl ", " analytics ", " analysis "]
engineering = [" eng ", " engineering ", " aero ", " aeronautical ", " mech ", " mechanical ", " ae ", " me ", " civil ", " auto ", " ece ", " electronics ", " robotics ", " ee ", " electrical ", " ce ", " mechatronics "]
science = ["sciences", "phy", "physics", "chem", "chemistry", "bio", "biology", "biomedical", "maths", "mathematics", "stats", "statistics", "finance", "mfe", "psychology", "psy", "psyc", "criminal"]
other = [" social ", " genetic ", " modelling "]

for i in range (len(new_df)):
  text = (str(new_df.iloc[i]['title']) + str(new_df.iloc[i]['selftext'])).lower()
  titles.append(new_df.iloc[i]['title'])
  scores.append(new_df.iloc[i]['score']) 
  data.append(new_df.iloc[i]['selftext'])
  #flair.append(submission.link_flair_text)
  links.append(len(re.findall(r'(https?://[^\s]+)', text)))

  time=new_df.iloc[i]['created_utc']
  date2=str(datetime.datetime.fromtimestamp(time))
  datem = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
  month.append(datem.month)
  year.append(datem.year)     

  if any(ele in text for ele in computerScience):
      domain.append("cs")
  elif any(ele in text for ele in engineering):
      domain.append("eng")
  elif any(ele in text for ele in science):
      domain.append("science")
  elif any(ele in text for ele in other):
      domain.append("other")
  else:
      domain.append("none")
  try:
    img.append(new_df.iloc[i]['post_hint'])

  except:
    img.append("none")

  if (' phd' in text and ' ms' in text) :
    degree.append('both')
  elif ' phd' in text:
    degree.append('phd')
  elif ' ms' in text:
    degree.append('ms')
  else:
    degree.append('none')
  word_count.append(len((text).split()))

print(new_df.iloc[550])

print(df.iloc[550])

import pandas as pd

df = pd.DataFrame()
inp = pd.DataFrame()

inp['title'] = titles
df['upvotes'] = scores 
df['month']=month # to do: extract month and day?
df['year'] = year
inp['data']=data
#df['flair']=flair
df['links']=links
df['img']=img
df['degree']=degree
df['domain']=domain
df['word_count']=word_count

print(df.shape)
df.head(10)

print(len(new_df))
print(inp.shape)

df.to_csv('df.csv', sep='\t')
inp.to_csv('inp.csv', sep='\t')

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.DataFrame()
inp = pd.DataFrame()
path = "/content/drive/MyDrive/df.csv"
df = pd.read_csv(path, sep='\t')

path_inp = "/content/drive/MyDrive/inp.csv"
inp = pd.read_csv(path_inp, sep='\t')

print(df.head())

df['img'] = df['img'].fillna("empty")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNetCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
import warnings
warnings.filterwarnings('ignore')

cat_cols=['year','degree','domain', 'month','img']
bool_cols=[]
numeric_cols=['upvotes', 'links', 'word_count']

lb = LabelBinarizer()
cat = [lb.fit_transform(df[col]) for col in cat_cols]
bol = [df[col].astype('int') for col in bool_cols]
t = df.loc[:, numeric_cols].values
final = [t] + cat
# y = df.score.values
x = np.column_stack(tuple(final))

print(df.head(5))

x[0]

#df['year'] = df['year'].astype("category")
df['degree'] = df['degree'].astype("category")
df['domain'] = df['domain'].astype("category")
df['month'] = df['month'].astype("category")
df['img'] = df['img'].astype("category")

#df['year'] = df['year'].cat.codes
df['degree'] = df['degree'].cat.codes
df['domain'] = df['domain'].cat.codes
df['month'] = df['month'].cat.codes
df['img'] = df['img'].cat.codes

df.head(5)
