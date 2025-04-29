#pip install pandas nltk Sastrawi

import pandas as pd
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_csv('./Dataset/data_test.csv')

factory = StemmerFactory()
stemmer = factory.create_stemmer()

stop_words = set(stopwords.words('indonesian'))

def preprocess(text):
    #1. Case folding
    text = text.lower()

    #2 Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    #3. Tokenizing
    tokens =  word_tokenize(text)

    #4. Stopword removal
    tokens = [word for word in tokens if word not in stop_words]

    #5. Stemming
    tokens = [stemmer.stem(word) for word in tokens]

    #Menggabungkan kembali hasil token jadi 1 string

    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

    # Menerapkan pra proses ke judul dan abstrak

df['Preprocessed_Judul'] = df['Judul'].apply(preprocess)
df['Preprocessed_Abstrak'] = df['Abstrak'].apply(preprocess)

df.to_csv('preprocessed_datatest.csv', index=False, encoding='utf-8-sig')

print("✅ Preprocessing selesai dan disimpan di 'preprocessed_datatest.csv'")

