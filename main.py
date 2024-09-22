# # Python program to translate
# # speech to text and text to speech
#
#
# import speech_recognition as sr
# import pyttsx3
#
# # Initialize the recognizer
# r = sr.Recognizer()
#
#
# # Function to convert text to
# # speech
# def SpeakText(command):
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()
#
#
# # Loop infinitely for user to
# # speak
#
# while (1):
#
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
#
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
#
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level
#             r.adjust_for_ambient_noise(source2, duration=0.2)
#
#             # listens for the user's input
#             audio2 = r.listen(source2)
#
#             # Using google to recognize audio
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()
#
#             print("Did you say ", MyText)
#             SpeakText(MyText)
#
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#
#     except sr.UnknownValueError:
#         print("unknown error occurred")
import random
import json
import pickle
import numpy as np
import nltk
import pyttsx3
import keras
import speech_recognition as sr
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
r = sr.Recognizer()
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = keras.models.load_model('chatbot.keras')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result


def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


print('Bot is running, speak quit or exit whenever you wish to close the chat')

while True:
    try:
        with sr.Microphone() as source2:

            r.adjust_for_ambient_noise(source2, duration=0.2)

            audio2 = r.listen(source2)

            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            if MyText == 'quit' or MyText == 'exit':
                break
            ints = predict_class(MyText)
            res = get_response(ints, intents)
            speak_text(res)
            print({'question': MyText, 'answer': res})
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
