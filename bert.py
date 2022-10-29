# -*- coding: utf-8 -*-
"""bert.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BfZODIQFKrCvlJUkyMMMEkr1pBT8T4sx
"""

!pip install transformers

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.metrics import confusion_matrix, accuracy_score

import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from keras.models import Model
from tensorflow.keras import utils as np_utils
from keras.utils.np_utils import to_categorical

import transformers
from transformers import AutoTokenizer,TFDistilBertModel, DistilBertConfig
from transformers import TFAutoModel

import warnings
warnings.filterwarnings("ignore")

print(tf.__version__)
print(keras.__version__)

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.DataFrame()
inp = pd.DataFrame()
path = "/content/drive/MyDrive/df.csv"
df = pd.read_csv(path, sep='\t')

path_inp = "/content/drive/MyDrive/inp.csv"
inp = pd.read_csv(path_inp, sep='\t')

inp.head()

df1.head()

df1=df[['upvotes']].copy()
df2=inp[['title']].copy()
df3=inp[['data']].copy()

up=[]
for i in range(len(df1)):
  if df1.iloc[i]['upvotes']<3:
    up.append("zero")
  elif df1.iloc[i]['upvotes']<10:
    up.append("zero_1")
  elif df1.iloc[i]['upvotes']<50:
    up.append("one")
  elif df1.iloc[i]['upvotes']<100:
    up.append("two")
  elif df1.iloc[i]['upvotes']<150:
    up.append("three")
  elif df1.iloc[i]['upvotes']<200:
    up.append("four")
  elif df1.iloc[i]['upvotes']<250:
    up.append("five")
  elif df1.iloc[i]['upvotes']<300:
    up.append("six")
  elif df1.iloc[i]['upvotes']<350:
    up.append("seven")
  elif df1.iloc[i]['upvotes']<400:
    up.append("eight")
  elif df1.iloc[i]['upvotes']<450:
    up.append("nine")
  elif df1.iloc[i]['upvotes']<500:
    up.append("ten")
  else:
    up.append("chad")

titles=[]
for i in range (len(df2)):
  titles.append(str(df2.iloc[i]['title'])+" "+str(df3.iloc[i]['data']))

data = pd.DataFrame()

data['input'] = titles
data['upvotes']=up

data.head(100)

X = data['input']
y = data['upvotes']

X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.2, random_state = 0)

encoder = LabelEncoder()
encoder.fit(y_train)

y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)

num_classes = np.max(y_train) + 1
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

bert = TFAutoModel.from_pretrained('distilbert-base-uncased')

for layer in bert.layers:
      layer.trainable = True

def text_encode(text, tokenizer, max_len=100):
    tokens = text.apply(lambda x: tokenizer(x,return_tensors='tf', 
                                            truncation=True,
                                            padding='max_length',
                                            max_length=max_len, 
                                            add_special_tokens=True))
    input_ids= []
    attention_mask=[]
    for item in tokens:
        input_ids.append(item['input_ids'])
        attention_mask.append(item['attention_mask'])
    input_ids, attention_mask=np.squeeze(input_ids), np.squeeze(attention_mask)

    return [input_ids,attention_mask]

X_train_input_ids, X_train_attention_mask = text_encode(X_train, tokenizer, max_len=100)
X_test_input_ids, X_test_attention_mask = text_encode(X_test, tokenizer, max_len=100)

def build_model(bert_model, maxlen=100):
   input_ids = tf.keras.Input(shape=(maxlen,),dtype=tf.int32, name='input_ids')
   attention_mask = tf.keras.Input(shape=(maxlen,),dtype=tf.int32, name='attention_mask')

   sequence_output = bert_model(input_ids,attention_mask=attention_mask)
   output = sequence_output[0][:,0,:]
   output = tf.keras.layers.Dense(32,activation='relu')(output)
   output = tf.keras.layers.Dropout(0.2)(output)
   output = tf.keras.layers.Dense(13,activation='softmax')(output)

   model = tf.keras.models.Model(inputs = [input_ids,attention_mask], outputs = [output])
   model.compile(Adam(lr=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

   return model

model = build_model(bert, maxlen=100)

history = model.fit(
    [X_train_input_ids, X_train_attention_mask],
    y_train,
    batch_size=32,
    validation_data=([X_test_input_ids, X_test_attention_mask], y_test),
    epochs=10
)

def plot_graphs(history, string):
  plt.plot(history.history[string])
  plt.plot(history.history['val_'+string])
  plt.xlabel("Epochs")
  plt.ylabel(string)
  plt.legend([string, 'val_'+string])
  plt.show()

plot_graphs(history, "accuracy")
plot_graphs(history, "loss")

loss, accuracy = model.evaluate([X_test_input_ids, X_test_attention_mask], y_test)
print('Test accuracy :', accuracy)
