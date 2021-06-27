import tkinter as tk
import speech_recognition as sr
from PIL import Image
import webbrowser
import os
import pathlib
from re import search
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

window = tk.Tk()
window.title("Seminars in AI")
window.geometry('400x200')
window.configure(background='gold')
mic = sr.Microphone()
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
# getting the text from the microphone and print it
def listen():
    # r = sr.Recognizer()
    # with mic as source:
    #     audio = r.listen(source)
    # text = r.recognize_google(audio)
    text = "I go to school"
    words = word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in words] #we get the stemmed version of the words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    try:
        finImg = Image.new('RGB', (512, 512))
        imageList = [] 
        openedImages = [] 
        currentChar = 0
        print(stemmed_words)
        for t in stemmed_words:
            if search("what are you doing", text):
                pass
            if pathlib.Path(f"./dataset/{t}.png").exists():
                print(t)
                imageList.append(f"./dataset/{t}.png")
            else:            
                for char in t:
                    if char  == " ":
                        char = "space"
                    imageList.append(("./dataset/alphabet/{}.png").format(char.lower()))
                    currentChar += 1
        for x in imageList:
            openedImages.append(Image.open(x)) 
        finImg.save("out.gif", save_all=True, append_images=openedImages, duration=600, loop=0)
        webbrowser.open("file:///" + os.path.realpath("out.gif")) 
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)


photo = tk.PhotoImage(file=r"./static/images/mic.png")
photo = photo.subsample(10, 10)
button = tk.Button(window, text='Listen', image=photo,
                   command=listen)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
