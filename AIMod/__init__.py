import os
import nltk
import playsound
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import re
import random
from paddlespeech.cli.tts.infer import TTSExecutor
import playsound

# Set the environment variable to disable oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# Load the pre-trained model and data
def load_data(data_path):
    try:
        model = load_model(data_path + 'chatbot_model.h5')
        # Compile the model with the desired loss and metrics
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        with open(data_path + 'intents.json', 'r', encoding="utf-8") as file:
            intents = json.load(file)
        words = pickle.load(open(data_path + 'words.pkl', 'rb'))
        classes = pickle.load(open(data_path + 'classes.pkl', 'rb'))
        return model, intents, words, classes
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None


# Preprocess the sentence
def preprocess_sentence(sentence):
    # Remove punctuation at the end of the sentence
    sentence = re.sub(r'[^\w\s]', '', sentence)
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)
    # Lemmatize each token
    lemmatized_tokens = [WordNetLemmatizer().lemmatize(token.lower()) for token in tokens]
    return lemmatized_tokens


# Create a bag of words
def create_bag_of_words(sentence, words):
    sentence_tokens = preprocess_sentence(sentence)
    bag = [0] * len(words)
    for token in sentence_tokens:
        for index, word in enumerate(words):
            if word == token:
                bag[index] = 1
    return np.array(bag)


# Predict the class
def predict_class(sentence, model, words, classes):
    bag_of_words = create_bag_of_words(sentence, words)
    prediction = model.predict(np.array([bag_of_words]))[0]
    # 调整阈值
    threshold = 0.05  # 降低阈值
    results = [[index, probability] for index, probability in enumerate(prediction) if probability > threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    print(f"Model predictions: {results}")
    return [{"intent": classes[index], "probability": str(probability)} for index, probability in results]


def get_response(intents, intents_data):
    if not intents:
        return "I'm sorry, but I didn't understand that."

    tag = intents[0]['intent']
    for intent in intents_data['intents']:
        if intent['tag'] == tag:
            # 使用正则表达式匹配模式
            for pattern in intent['patterns']:
                # 优化正则表达式
                # 注意：这里假设输入文本和模式都是简单的单词或短语，因此直接使用简单的字符串比较
                if pattern.lower() == input_text.lower():
                    return random.choice(intent['responses'])
    return "I'm sorry, but I didn't understand that."


# Function to get the AI output
def AIOutput(input, data_path):
    print(data_path)
    global input_text  # 添加全局变量声明
    input_text = input  # 保存输入文本用于正则表达式匹配
    model, intents_data, words, classes = load_data(data_path)
    if model is None or intents_data is None or words is None or classes is None:
        return "Failed to load necessary data."

    intents = predict_class(input, model, words, classes)
    print(intents)
    response = get_response(intents, intents_data)
    tts = TTSExecutor()
    tts(response, speed=1.0, language="zh", model="speedyspeech_csmsc", output="./output.wav")
    return response, "./output.wav"


# Example usage
if __name__ == "__main__":
    while True:
        input_text = input("Player: ")
        output, wav_output = AIOutput(input_text, os.getcwd() + "\\")
        print("Bot: " + output)
        playsound.playsound(wav_output)


def AIBot(input_text):
    output_text = AIOutput(input_text, os.getcwd() + "/AIMod/")
    return output_text
