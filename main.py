import tkinter as tk
import speech_recognition as sr
from PIL import Image
import webbrowser
import os
import pathlib
import nltk
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pygame
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
#from re import search

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
    r = sr.Recognizer()
    with mic as source:
        audio = r.listen(source)
    text = r.recognize_google(audio)
    #text = "I go to supermarket."
    words = word_tokenize(text)
    words=[word.lower() for word in words if word.isalpha()]
    stemmed_words = [stemmer.stem(word) for word in words] #we get the stemmed version of the words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    try:
        returnedImage = Image.new('RGB', (512, 512))
        imageList = [] 
        finalImages = [] 
        currentChar = 0
        print(stemmed_words)
        for t in stemmed_words:
            if pathlib.Path(f"./dataset/{t}.png").exists():
                print(t)
                imageList.append(f"./dataset/{t}.png")
            else:            
                for char in t:
                    imageList.append(("./dataset/alphabet/{}.png").format(char.lower()))
                    currentChar += 1
        for x in imageList:
            finalImages.append(Image.open(x)) 
        print(imageList)
        returnedImage.save("out.gif", save_all=True, append_images=finalImages, duration=600, loop=0)
        webbrowser.open("file:///" + os.path.realpath("out.gif")) 
    except:
        print("There was problem with understanding the audio. Try again.")

photo = tk.PhotoImage(file=r"./static/images/mic.png")
photo = photo.subsample(10, 10)
button = tk.Button(window, text='Listen', image=photo,
                   command=listen)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
