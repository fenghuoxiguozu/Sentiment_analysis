import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Embedding,BatchNormalization
from keras.layers.recurrent import SimpleRNN,LSTM
from keras.layers import Dense,Dropout,Flatten
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import Adam

maxlen=80  #向量维度
num_words=2000 #索引字典长度
epochs=50 #训练次数

df=pd.read_csv(r'F:\keras\Sentiment_analysis\dataset\clean_data.csv',names=None)
all_texts=df['content'].tolist()

tokenizer=Tokenizer(num_words=num_words,filters='%')
tokenizer.fit_on_texts(all_texts)
np.save('F:\keras\Sentiment_analysis\dataset\words_dict.npy',tokenizer.word_index)
sequences=tokenizer.texts_to_sequences(all_texts)
vocab_size=len(tokenizer.word_index)+1 #得到每个词的编号
print('vocab_size:',vocab_size)
X=pad_sequences(sequences,padding='post',maxlen=maxlen) #将超过固定值的部分截掉，不足的在最前面用0填充
#评分必须从0开始  0：好评 1：差评  2：中评
df['score']=df['score'].replace(3,0)
Y=np_utils.to_categorical(df['score'].values,num_classes=3)
print(X.shape,Y.shape)  # (82427, 80) (82427, 3)


model=Sequential()
model.add(Embedding(input_dim=num_words,output_dim=128,input_length=maxlen))
model.add(LSTM(128,dropout=0.2,recurrent_dropout=0.2))
model.add(Dense(units=3,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.001),metrics=['accuracy'])
history=model.fit(X,Y,epochs=epochs,batch_size=128,validation_split=0.1)
loss1,acc1=model.evaluate(X,Y)
print('训练集准确度：',acc1)
model.summary()
model.save(r'F:\keras\Sentiment_analysis\dataset\model.h5')

#绘制 acc，loss
acc = history.history['acc']
loss = history.history['loss']
print(acc,loss)

x=range(1,epochs+1)
plt.plot(x,acc, 'r', label='Training acc')
plt.plot(x,loss, 'b', label='Training loss')
plt.title('Training acc and loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()