import jieba
jieba.load_userdict(r'F:\keras\Sentiment_analysis\dataset\userdict.txt')
import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


mod=load_model('F:\keras\Sentiment_analysis\model\model.h5')
dict=np.load('F:\keras\Sentiment_analysis\dataset\words_dict.npy').item()
df_stopwords=pd.read_table(r'F:\keras\Sentiment_analysis\stopwords.txt',names=['stopword'])
stopwords=df_stopwords['stopword'].tolist()

def clean(text):
    test_data = []
    texts = jieba.lcut(text)
    for text in texts:
        if text in stopwords:
            continue
        else:
            test_data.append(text)
    return test_data

def vec(clean_data):
    vec=[]
    for text in clean_data:
        try:
            if dict[text]<=2000:
                vec.append(dict[text])
            else:
                vec.append(0)
                # continue
        except:
            vec.append(0)
    return vec

if __name__ == '__main__':
    text = '购买日期是2019年2月7日，手机激活日期是2018年11月，我买的是二手机'
    clean_data=clean(text)
    vec=vec(clean_data)
    pad = pad_sequences([vec], maxlen=80, padding='post')
    result=mod.predict_classes(pad)
    if result==0:
        print(text,": 好评")
    elif result==1:
        print(text,": 差评")
    else:
        print(text,": 中评")



