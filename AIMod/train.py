import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

# 加载意图文件
intents_file = open('intents.json', 'r', encoding='utf-8').read()
intents = json.loads(intents_file)

# 数据预处理
words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']

lemmatizer = WordNetLemmatizer()

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # 分词
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        # 添加文档到语料库
        documents.append((word, intent['tag']))
        # 添加到类别列表
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# 对单词进行词形还原，并去除重复项
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))

# 排序类别
classes = sorted(list(set(classes)))

# 文档数量
print(len(documents), "documents")

# 类别数量
print(len(classes), "classes", classes)

# 唯一的词形还原后的单词数量
print(len(words), "unique lemmatized words", words)

# 保存词汇表和类别
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# 创建训练数据
training = []

# 创建空数组作为输出
output_empty = [0] * len(classes)

# 训练集，每个句子的词袋表示
for doc in documents:
    # 初始化词袋
    bag = []
    # 当前模式的分词列表
    word_patterns = doc[0]
    # 对每个词进行词形还原
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    # 创建词袋数组
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # 输出是一系列 '0'，对应类别的位置是 '1'
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    # 确保 bag 和 output_row 的长度一致
    assert len(bag) == len(words), f"Bag length mismatch: {len(bag)} vs {len(words)}"
    assert len(output_row) == len(classes), f"Output row length mismatch: {len(output_row)} vs {len(classes)}"

    # 将 bag 和 output_row 拼接成一个列表
    combined = bag + output_row
    training.append(combined)

# 打乱特征
random.shuffle(training)

# 将 training 转换为 numpy 数组
training = np.array(training)

# 创建训练和测试列表
train_x = training[:, :len(words)]  # 取 bag 部分
train_y = training[:, len(words):]  # 取 output_row 部分

# 手动划分训练集和验证集
test_size = 0.2
split_index = int(len(train_x) * (1 - test_size))

x_train, x_val = train_x[:split_index], train_x[split_index:]
y_train, y_val = train_y[:split_index], train_y[split_index:]

# 定义模型
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# 编译模型
# 更新 SGD 优化器初始化方式
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# 训练模型
hist = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10000, batch_size=5, verbose=1)

# 保存模型
model.save('chatbot_model.h5')

print("model is created")
