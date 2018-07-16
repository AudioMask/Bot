
# coding: utf-8

# In[8]:

import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import warnings
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')
types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}
 
def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out
 
def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"
 
    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)
 
wav = wave.open("3.wav")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
 
duration = nframes / framerate
w, h = 800, 300
k = int(nframes/w/32)
DPI = 72
peak = 256 ** sampwidth / 2
 
content = wav.readframes(nframes)
samples = np.fromstring(content, dtype=types[sampwidth])
 
plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)
 
for n in range(1):
    channel = samples[n::nchannels]
    channel = channel[0::k]
    if nchannels == 1:
        channel = channel - peak
 
    axes = plt.subplot(2, 1, n+1)
    axes.plot(channel, "g",linewidth=0.1)
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
    plt.grid(True, color="black")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())
axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("laugh")
plt.ylim(-75000,75000)
plt.show()


# In[79]:

import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import statsmodels
import statsmodels.api as sm
import statsmodels
import pandas as pd
import warnings
from tqdm import tqdm 
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')
def to_sprectrogram(z):
    types = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }

    def format_time(x, pos=None):
        global duration, nframes, k
        progress = int(x / float(nframes) * duration * k)
        mins, secs = divmod(progress, 60)
        hours, mins = divmod(mins, 60)
        out = "%d:%02d" % (mins, secs)
        if hours > 0:
            out = "%d:" % hours
        return out

    def format_db(x, pos=None):
        if pos == 0:
            return ""
        global peak
        if x == 0:
            return "-inf"

        db = 20 * math.log10(abs(x) / float(peak))
        return int(db)

    wav = wave.open(z)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    duration = nframes / framerate
    w, h = 800, 300
    k = int(nframes/w/32)
    DPI = 72
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.fromstring(content, dtype=types[sampwidth])

    plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
    plt.subplots_adjust(wspace=0, hspace=0)

    for n in range(1):
        channel = samples[n::nchannels]
        #channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak

        axes = plt.subplot(2, 1, n+1)
        axes.plot(channel, "m",linewidth=0.8)
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
        plt.grid(True, color="black")
        axes.xaxis.set_major_formatter(ticker.NullFormatter())
    axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    plt.show()
    plt.savefig("wave", dpi=DPI)
    return pd.DataFrame({'Frequency': pd.Series(channel), 'Time': pd.Series([i for i in range(1, len(channel)+1)])})
data_1 = to_sprectrogram('1.wav')
data_2 = to_sprectrogram('2.wav')
#data = data.drop(['Time'],axis=1)


# In[80]:

data.head()


# In[81]:

def Draw_autcorrelation(data,c = 'b'):
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(data, lags=50, ax=ax1,color=c)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(data, lags=50, ax=ax2,color=c)
    plt.show()
Draw_autcorrelation(data)


# In[82]:

df = pd.read_csv('workpls.csv', sep = ',', error_bad_lines=False)


# In[6]:

df.columns = ['ItemID','Sentiment','SentimentSource','SentimentText']


# In[ ]:




# In[7]:

df


# In[8]:

plus = 0
minus = 0
for i in tqdm(range(len(df))):
    if df['Sentiment'][i] == 1:
        plus += 1
    else:
        minus += 1
print(plus)
print(minus)


# In[9]:

from copy import copy
l = copy(df['SentimentText'][:10000])
for i in tqdm(range(10000)):
    l[i] = len(l[i].split())


# In[14]:

l = pd.Series(np.sort(np.array(l)))


# In[15]:

df_new = pd.DataFrame({'Sentiment' : df['Sentiment'][:10000], 'Num' : l})


# In[16]:

df_new


# In[17]:

plt.plot(df_new)


# In[4]:

import torch
import torchvision


# In[16]:

import os
thisFile = "work.mp3"
base = os.path.splitext(thisFile)[0]
os.rename(thisFile, base + ".wav")

