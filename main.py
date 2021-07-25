import tkinter as tk
import speech_recognition as sr
from PIL import Image
import webbrowser
import os
import pathlib
import nltk
import bs4
import requests
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
#from re import search

window = tk.Tk()
window.title("Speech to ASL")
window.geometry('400x200')
window.configure(background='gold')

nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def get_images():
    '''
    This function is used to get all the images from the website and add them to the local storage. 
    
    You just need to call the function to make it work. This function does not take any parameter.

    This function uses all english alphabet letters and for those letters checks the website and downloads the images.

    '''
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i','j', 'k', 'l','m', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for letter in letters:
        url = f'https://www.babysignlanguage.com/dictionary-letter/?letter={letter}'
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        content = str(soup.find_all('div', {"class": "single-letter-card"}))
        soup1 = bs4.BeautifulSoup(content, 'html.parser')
        hrefList = []
        for a in soup1.find_all('a', href=True):
            hrefList.append(a['href'])
        for href in hrefList:
            res = requests.get(href)
            soup2 = bs4.BeautifulSoup(res.text, 'html.parser')
            cnt = str(soup2.find_all('div', {"class": "hero-right"}))
            soup3 = bs4.BeautifulSoup(cnt, 'html.parser')
            for img in soup3.find_all('img'):
                imageInfo = img['src'].split('/')
                imageInfo = imageInfo[-1].split('.')
                image = Image.open(requests.get(f"https:{img['src']}", stream = True).raw)
                image = image.resize((512, 512), Image.ANTIALIAS)
                image.save(f'./new/{imageInfo[0]}.png')
# getting the text from the microphone and print it
NORM_FONT= ("Verdana", 10)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Output word")
    label = tk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    #popup.mainloop()

def listen():
    '''
    This is the main function we actually using for the application. 

    We are first getting the user input from the microphone and then apply NLP to it in order to first tokenize the words.

    Then we check if we have the tokenized word in our image database, so if there is an image in that words, it adds to the list. 

    '''
    # mic = sr.Microphone()
    # r = sr.Recognizer()
    # with mic as source:
    #     audio = r.listen(source)
    #text = r.recognize_google(audio)
    text = "Today I will plant trees in garden"
    #popupmsg(text)
    words = word_tokenize(text)
    print(words)
    words=[word.lower() for word in words if word.isalpha()]
    print(words)
    stop_words = set(stopwords.words("english"))
    stemmed_words = [stemmer.stem(word) for word in words] #we get the stemmed version of the words
    filtered_list = [word for word in stemmed_words if word.casefold() not in stop_words]
    print(stemmed_words)
    print(filtered_list)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    try:
        returnedImage = Image.new('RGB', (512, 512))
        imageList = [] 
        finalImages = [] 
        currentChar = 0
        for t in filtered_list:
            if pathlib.Path(f"./dataset/phases/{t}.png").exists():
                imageList.append(f"./dataset/phases/{t}.png")
            else:            
                for char in t:
                    imageList.append(("./dataset/alphabet/{}.png").format(char.lower()))
                    currentChar += 1
        for x in imageList:
            finalImages.append(Image.open(x)) 
        returnedImage.save("output.gif", save_all=True, append_images=finalImages, duration=600, loop=0)
        webbrowser.open("file:///" + os.path.realpath("output.gif")) 
    except:
        print("There was problem with understanding the audio. Try again.")

photo = tk.PhotoImage(file=r"./static/images/mic.png")
photo = photo.subsample(10, 10)
button = tk.Button(window, text='Listen', image=photo,
                   command=listen)
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
