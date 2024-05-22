from flask import Flask, render_template, request
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            lemmatized_text = lemmatize(text)
            filtered_text = stop_word_reducer(lemmatized_text)
            return render_template('result.html', text=text, lemmatized_text=lemmatized_text, filtered_text=filtered_text)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

def lemmatize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in tokens]
    lemmatized_text = ' '.join(lemmatized_text)
    print("Original text:", text)
    print("Lemmatized text:", lemmatized_text)
    return lemmatized_text

def stop_word_reducer(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_tokens)
    print(filtered_text)
    return filtered_text

if __name__ == '__main__':
    app.run(debug=True)
