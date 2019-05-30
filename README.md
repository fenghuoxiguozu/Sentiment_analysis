# 京东评论情感分析
是对带有情感色彩的主观性文本进行分析、处理、归纳和推理的过程。互联网(如博客和论坛以及社会服务网络如大众点评)上产生了大量的用户参与的、对于诸如人物、事件、产品等有价值的评论信息。这些评论信息表达了人们的各种情感色彩和情感倾向性,如喜、怒、哀、乐和批评、赞扬等。基于此,潜在的用户就可以通过浏览这些主观色彩的评论来了解大众舆论对于某一事件或产品的看法。
本项目对京东手机三分类进行情感分析。

# 工具 环境
Pycharm  python3.6 MySQL Redis

# 所需重要库
Scrapy Scrapy_redis Keras jieba pandas matplolib

# 流程
1. 爬虫：分布式爬取京东手机好评，中评，差评三种评论。数据保存至MySQL
2. 数据预处理：a. 对评论jieba分词，分词不太准确的用用户字典加载，消除歧义。
			  b. 对分词结果优化，部分空格日期等垃圾数据，再次清洗
			  c. woed_Embedding对词建立索引，保存数据
3. LSTM建模：训练50次，准确率达到85%+

# 重要过程实现
1. 京东评论网址：数据保存在json里，需对网址进行参数(productId,fetchJSON_comment98vv9547)拼接
e.g. https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv9547&productId=100003433872&score=3&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
productId: 商品ID,商品详情页URL上
comment: 网页源码搜索comment 

# 优化
1. 一般网购商品评论90%+都是好评，爬取数据时可以对好评数量进行限制，平衡样本。
2. 分词时英文词汇(vivo,ios)等基本无语义，所以全部删除，但部分词汇（e.g OK good）等对分析有重要影响。
