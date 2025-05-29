import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt

# 第零步 设置matplotlib的全局字体为SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 第一步 读取评论数据
df = pd.read_csv('DATA/comments.csv', index_col=0)

# 第二步 建立情感分数列表
sentiment_scores=[]

# 第三步 将每个评论进行情感计算
for comment in df['评论'] :

    # 创建snowNLP对象
    s=SnowNLP(comment)

    # 得到这个评论的情感得分(0~1)
    score = s.sentiments

    # 添加到情感分数列表种
    sentiment_scores.append(score)

# 第四步 导入情感得分到框架中
df['情感得分']=sentiment_scores


# 第五步 设定阈值，判断情绪类别
def classify_sentiment(score):
    if score > 0.6:
        return '正面'
    elif score < 0.4:
        return '负面'
    else:
        return '中性'

# 第六步 导入情绪进框架中
df['情绪'] = df['情感得分'].apply(classify_sentiment)


# 第七步 保存新 CSV
# 删除 '时间' 这一列
df.drop(columns=['时间'], inplace=True)
df.to_csv('DATA/comments_with_sentiment.csv', index=False)




# 统计每类情绪数量
sentiment_counts = df['情绪'].value_counts()

# 画饼图
plt.figure(figsize=(6, 6))
plt.pie(
    sentiment_counts.values,              # 每块的大小
    labels=sentiment_counts.index,        # 每块对应的标签（情绪类型）
    autopct='%1.1f%%',                    # 显示百分比，保留一位小数
    colors=['green', 'gray', 'red'],      # 各情绪的颜色
    startangle=140                        # 起始角度，让图更美观
)
plt.title('情绪分布比例图')
plt.axis('equal')  # 让饼图是圆的
plt.tight_layout()
plt.show()












