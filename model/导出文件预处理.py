import pandas as pd

df=pd.read_csv('F:\keras\Sentiment_analysis\dataset\clean_data.csv')
print("去除空行前shape",df.shape)
df=df.dropna()
df=df[df['content'].str.strip()!='']
print("去除空行后shape",df.shape)
df.to_csv('F:\keras\Sentiment_analysis\dataset\clean_data.csv',index=False)
print('数据评论预处理成功')