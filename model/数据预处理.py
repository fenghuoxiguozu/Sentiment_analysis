import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import re
import jieba
jieba.load_userdict(r'F:\keras\Sentiment_analysis\dataset\userdict.txt')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签


#打开neg pos stopwords
df_comment=pd.read_csv(r'F:\keras\Sentiment_analysis\dataset\jd_comment.csv')
df_stopwords=pd.read_table(r'F:\keras\Sentiment_analysis\dataset\stopwords.txt',names=['stopword'])
stopwords=df_stopwords['stopword'].tolist()
df_comment=shuffle(df_comment)

def drawing_score():
    score_num=df_comment['score'].value_counts()
    plt.bar(score_num.index,score_num.values,color='#4F94CD',label='京东手机评分图')
    plt.xlim(0,4)
    plt.ylim(10000,35000)
    plt.legend(loc='upper left')
    plt.show()

def stop(Comments):
    cleandata = []
    for comment in Comments:
        if comment.strip() in stopwords or comment==' ':
            continue
        cleandata.append(comment.strip())
    return cleandata

def drawing_word_length():
#查看字符长度分布
    length=np.array([len(x) for x in df_comment['content']])
    plt.hist(length, bins=200)
    plt.xlim((0, 300))
    plt.ylabel('number of Distribution')
    plt.xlabel('length of Distribution')
    plt.title('Distribution of length')
    plt.show()

df_comment['content']=df_comment['content'].astype(str).apply(lambda x:jieba.lcut(x))
print('分词成功')
df_comment['content']=df_comment['content'].apply(stop)
print('加载停用词成功')
df_comment['content']=df_comment['content'].apply(lambda x:' '.join(x))
df_comment['content']=df_comment['content'].apply(lambda x:re.sub(r'[a-zA-Z0-9\.]','',x))
df_comment.to_csv('F:\keras\Sentiment_analysis\dataset\clean_data.csv',index=False)


drawing_word_length()
#每条字符长度基本都在200左右