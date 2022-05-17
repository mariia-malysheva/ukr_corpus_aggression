# ukr_corpus_aggression



Ukrainian-language corpus of aggressive texts of network discourse.



censor-parser.py - scraping comments from Censor.Net (it is necessary to specify the number of pages and language of comments, additionally determines the polarity);

comment_corpus.csv - a corpus of comments collected using censor-parser.py, the author's nickname, comment text, language and polarity (ukr, negative);

preprocessing.py - additional processing of comments (text cleaning, tokenization, lemmatization, removal of stop words, bigram, statistics);

change_token.csv - dictionary for additional lemmatization;

stopwords_ua.txt - list of stop words (https://github.com/skupriienko/Ukrainian-Stopwords), slightly updated;



Українськомовний корпус агресивних текстів мережевого дискурсу.



censor-parser.py - парсинг коментарів з Цензор.Net (необхідно вказати кількість сторінок та мову коментарів, додатково визначає полярність);

comment_corpus.csv - корпус коментарів, зібраних за допомогою censor-parser.py, зазначено нікнейм автора, текст коментаря, мову та полярність (укр, негативна);

preprocessing.py - додаткова обробка коментарів (очищення текстів, токенізація, лематизація, видалення стоп-слів, біграми, статистика);

change_token.csv - словник для додаткової лематизації;

stopwords_ua.txt - список стоп-слів ( https://github.com/skupriienko/Ukrainian-Stopwords ), трішечки доповнений;


