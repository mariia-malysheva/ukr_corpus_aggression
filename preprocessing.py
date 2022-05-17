import pandas as pd
import re
import simplemma
from simplemma import text_lemmatizer
from simplemma import simple_tokenizer
from nltk import FreqDist
import nltk

#Читаємо файл у датафрейм
comments = pd.read_csv('comment_corpus.csv', sep=';', usecols=['Text']).drop_duplicates(subset=['Text'])
comments = pd.DataFrame.to_string(comments)
comments = re.sub(r'[a-zA-Z_]+|[^\w\s]+|[\d]+', r'',comments).lower()

#Завантажуємо дані токенізатора й лематизатора
languageData = simplemma.load_data('uk')

#Токенізуємо
tokens = simple_tokenizer(comments)
ntokens= len(tokens) #кількість токенів у корпусі
utokens = len(set(tokens)) #кількість унікальних токенів у корпусі без повторів

#Створюємо частотний словник СЛОВОФОРМ (токенів)
wordList = pd.DataFrame(tokens, columns=['token']) #словник токенів
afreq = wordList.count()[0]
wordList = wordList['token'].value_counts().to_frame().reset_index()
wordList['relat_freq'] = wordList['token']/afreq
wordList.columns = ['token', 'absol_freq', 'relat_freq']
wordList.to_csv('token-list-with-stopwords.csv', sep=';')

#Лематизуємо
lemas = text_lemmatizer(comments, languageData, greedy=True) #початковий список лем

#Читаємо дані додаткового етапу лематизації із файлу у словник
extraLemaDict = pd.read_csv('change_token.csv', header=None, index_col=0, squeeze=True).to_dict()
#Додаткова лематизація
extraLemmatize = pd.Series(lemas)
#Змінюємо за словником, відсутні на старі значення
extraLemmatize = extraLemmatize.map(extraLemaDict).fillna(extraLemmatize)
extraLemmatize = extraLemmatize.values.tolist() #кінцевий список лем

#Кількість унікальних лем
nlema = len(set(extraLemmatize)) #кількість унікальних лем
#Індекс різномантіності (багатство словника)
diversityIndex = nlema/ntokens #індекс різноманітності (багатство словника)
#Середня повторюваність слова у корпусі
repeatIndex = ntokens/nlema #середня повторюваність слова у корпусі

#Кількість слів з частотою 1
dfreqwords = FreqDist(extraLemmatize) 
dhapaxLegomena = len([w for w in dfreqwords if dfreqwords[w] == 1]) #кількість слів з частотою 1 у словнику лем
cfreqwords = FreqDist(tokens)
chapaxLegomena = len([w for w in cfreqwords if cfreqwords[w] == 1]) #кількість слів з частотою 1 у корпусі

#Індекс винятковості
dexclusivityIndex = dhapaxLegomena/nlema #індекс винятковості у словнику лем
cexclusivityIndex = chapaxLegomena/ntokens #індекс винятковості у корпусі

#Індекс концентрації
dmostfreq = len([w for w in dfreqwords if dfreqwords[w] > 10]) #кількість слів з частотою більше 10 у словнику лем
cmostfreq = len([w for w in cfreqwords if cfreqwords[w] > 10]) #кількість слів з частотою більше 10 у корпусі
cconcentrIndex = cmostfreq/ntokens #індекс концентрації в корпусі
dconcentrIndex = dmostfreq/nlema #індекс концентрації в словнику лем

#Створюємо частотний словник СЛІВ (лем)
lemmasList = pd.DataFrame(extraLemmatize, columns=['Lema with stop-words']) #словник лем
afreq = lemmasList.count()[0]
lemmasList = lemmasList['Lema with stop-words'].value_counts().to_frame().reset_index()
lemmasList['relat_freq'] = lemmasList['Lema with stop-words']/afreq
lemmasList.columns = ['lema', 'absol_freq', 'relat_freq']
lemmasList.to_csv('lemmas-list-with-stopwords.csv', sep=';')

####################
####################

#СТОП-СЛОВА
#Читаємо стоп-слова у список
stopwords_ua = pd.read_csv("stopwords_ua.txt", header=None, names=['stopwords'])
stopWords = list(stopwords_ua.stopwords)

#Видаляємо стоп-слова
tokensWithoutStopWords = [word for word in tokens if word not in stopWords] #видаляємо стоп-слова в корпусі
ntokensWithoutStopWords = len(tokensWithoutStopWords) #кількість токенів без стоп-слів
utokensWithoutStopWords = len(set(tokensWithoutStopWords)) #кількість унікальних токенів без стоп-слів
lemasWithoutStopWords = [word for word in extraLemmatize if word not in stopWords] #видаляємо стоп-слова в словнику лем
nlemasWithoutStopWords = len(set(lemasWithoutStopWords)) #кількість унікальних лем без стоп-слів

#Створюємо частотний словник СЛОВОФОРМ (токенів)
wordListWithoutStopWords = pd.DataFrame(tokensWithoutStopWords, columns=['token']) #словник токенів
afreqWithoutStopWords = wordListWithoutStopWords.count()[0]
wordListWithoutStopWords = wordListWithoutStopWords['token'].value_counts().to_frame().reset_index()
wordListWithoutStopWords['relat_freq'] = wordListWithoutStopWords['token']/afreqWithoutStopWords
wordListWithoutStopWords.columns = ['token', 'absol_freq', 'relat_freq']
wordListWithoutStopWords.to_csv('token-list-without-stopwords.csv', sep=';')

#Індекс різномантіності (багатство словника)
diversityIndexWithoutStopWords = nlemasWithoutStopWords/ntokensWithoutStopWords #індекс різномантіності без стоп-слів
#Середня повторюваність слова у корпусі
repeatIndexWithoutStopWords = ntokensWithoutStopWords/nlemasWithoutStopWords #середня повторюваність слова у корпусі без стоп-слів

#Кількість слів з частотою 1
dfreqwordsWithoutStopWords = FreqDist(lemasWithoutStopWords) 
dhapaxLegomenaWithoutStopWords = len([w for w in dfreqwordsWithoutStopWords if dfreqwordsWithoutStopWords[w] == 1]) #кількість слів з частотою 1 в словнику лем без стоп-слів
cfreqwordsWithoutStopWords = FreqDist(tokens)
chapaxLegomenaWithoutStopWords = len([w for w in cfreqwordsWithoutStopWords if cfreqwordsWithoutStopWords[w] == 1]) #кількість слів з частотою 1 в корпусі без стоп-слів

#Індекс винятковості
cexclusivityIndexWithoutStopWords = chapaxLegomenaWithoutStopWords/ntokensWithoutStopWords #індекс винятковості в корпусі без стоп-слів
dexclusivityIndexWithoutStopWords = dhapaxLegomenaWithoutStopWords/nlemasWithoutStopWords #індекс винятковості в словнику лем без стоп-слів

#Індекс концентрації
dmostfreqWithoutStopWords = len([w for w in dfreqwordsWithoutStopWords if dfreqwordsWithoutStopWords[w] > 10]) #кількість слів з частотою більше 10 у словнику лем без стоп-слів
cmostfreqWithoutStopWords = len([w for w in cfreqwordsWithoutStopWords if cfreqwordsWithoutStopWords[w] > 10]) #кількість слів з частотою більше 10 у корпусі без стоп-слів
cconcentrIndexWithoutStopWords = cmostfreqWithoutStopWords/ntokens #індекс концентрації в корпусі без стоп-слів
dconcentrIndexWithoutStopWords = dmostfreqWithoutStopWords/nlemasWithoutStopWords #індекс концентрації в словнику лем без стоп-слів

##Створюємо частотний словник СЛІВ (лем) без стоп-слів
lemmasListWithoutStopWords = pd.DataFrame(lemasWithoutStopWords, columns=['Lema without stop-words']) #словник лем
afreqWithoutStopWords = lemmasListWithoutStopWords.count()[0]
lemmasListWithoutStopWords = lemmasListWithoutStopWords['Lema without stop-words'].value_counts().to_frame().reset_index()
lemmasListWithoutStopWords['relat_freq'] = lemmasListWithoutStopWords['Lema without stop-words']/afreqWithoutStopWords
lemmasListWithoutStopWords.columns = ['lemma', 'absol_freq', 'relat_freq']
lemmasListWithoutStopWords.to_csv('lemmas-list-without-stopwords.csv', sep=';')

###################
###################

#БІГРАМИ
#Створюємо частотний словник СЛОВОСПОЛУЧЕНЬ (біграмів)
bigramm=nltk.ngrams(lemasWithoutStopWords,2, right_pad_symbol=';')
bigramm=nltk.FreqDist(bigramm)
bigrammCommon = bigramm.most_common()
bigrammTable = pd.DataFrame(bigrammCommon, columns=['Bigram', 'absol_freq'])
bigrammTable.to_csv('bigramms-list.csv', sep=';')

###################
###################

#СТАТИСТИЧНІ ХАРАКТЕРИСТИКИ

statistics = pd.DataFrame({'Кількість слів у корпусі': [ntokens, ntokensWithoutStopWords], \
    'Кількість унікальних словоформ': [utokens, utokensWithoutStopWords], \
    'Розмір словника': [nlema, nlemasWithoutStopWords], \
    'Індекс різноманітності': [diversityIndex, diversityIndexWithoutStopWords], \
    'Індекс повторюваності слів': [repeatIndex, repeatIndexWithoutStopWords],
    'Кількість слів з частотою 1 у корпусі': [chapaxLegomena, chapaxLegomenaWithoutStopWords] , \
    'Кількість слів з частотою 1 у словнику': [dhapaxLegomena, dhapaxLegomenaWithoutStopWords], \
    'Індекс винятковості у корпусі': [cexclusivityIndex, cexclusivityIndexWithoutStopWords], \
    'Індекс винятковості у словнику': [dexclusivityIndex, dexclusivityIndexWithoutStopWords], \
    'Кількість слів з частотою більше 10 у корпусі': [cmostfreq, cmostfreqWithoutStopWords], \
    'Кількість слів з частотою більше 10 у словнику': [dmostfreq, dmostfreqWithoutStopWords], \
    'Індекс концентрації у корпусі': [cconcentrIndex, cconcentrIndexWithoutStopWords], \
    'Індекс концентрації у словнику': [dconcentrIndex, dconcentrIndexWithoutStopWords]}, index=['Зі стоп-словами', 'Без стоп-слів'])
statistics.to_csv('statistics.csv', sep=';')



