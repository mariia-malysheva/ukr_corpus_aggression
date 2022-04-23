import pandas as pd
import re
import simplemma
from simplemma import text_lemmatizer
from nltk import FreqDist
import nltk

#Чтение файла в датафрейм
aggressiveComment = pd.read_csv('comment_corpus.csv', sep=';', usecols=['Text']).drop_duplicates(subset=['Text'])
aggressiveComment = pd.DataFrame.to_string(aggressiveComment)
aggressiveComment = re.sub(r'[a-zA-Z_]+|[^\w\s]+|[\d]+', r'',aggressiveComment).lower()
#Загрузка данный лемматизатора
languageData = simplemma.load_data('uk')
#Лемматизация
aggressiveCommentLemma = text_lemmatizer(aggressiveComment, languageData, greedy=True)
#Чтение стоп-слов в список
stopwords_ua = pd.read_csv("stopwords_ua.txt", header=None, names=['stopwords'])
stopWords = list(stopwords_ua.stopwords)
#Удаление стоп-слов
aggressiveCommentWithoutStopWords = [word for word in aggressiveCommentLemma if word not in stopWords]

#Чтение данных долемматизации из файла в словарь
extraLemmatizeDict = pd.read_csv('change_token.csv', header=None, index_col=0, squeeze=True).to_dict()

#Долемматизация
extraLemmatize = pd.Series(aggressiveCommentWithoutStopWords)
#Замена по словарю, отсутствующие обратно на старые значения
extraLemmatize = extraLemmatize.map(extraLemmatizeDict).fillna(extraLemmatize)
extraLemmatize = extraLemmatize.values.tolist()

#Рассчет частоты
aggressiveToken = FreqDist(extraLemmatize)
aggressiveTokenCommon = aggressiveToken.most_common()
tokenTable = pd.DataFrame(aggressiveTokenCommon, columns=['Word', 'Frecuency'])
tokenTable.to_csv('lemmas.csv', sep=';')

bigramm=nltk.ngrams(extraLemmatize,2, right_pad_symbol=';')
bigramm=nltk.FreqDist(bigramm)
bigrammCommon = bigramm.most_common()
bigrammTable = pd.DataFrame(bigrammCommon, columns=['Bigramm', 'Frecuency'])
bigrammTable.to_csv('bigramms.csv', sep=';')

