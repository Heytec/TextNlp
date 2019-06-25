#Text summarization is a subdomain of Natural Language Processing (NLP) that deals with extracting summaries from huge chunks of texts.
# There are two main types of techniques used for text summarization: NLP-based techniques and deep learning-based techniques.
     # steps :
# 1)Convert Paragraphs to Sentences - The most common way of converting paragraphs to sentences is to split the paragraph whenever a period is encountered
# 2)Text Preprocessing After converting paragraph to sentences, we need to remove all the special characters, stop words and numbers from all the sentences
# 3)Tokenizing the Sentences  - We need to tokenize all the sentences to get all the words that exist in the sentences
# 4)Find Weighted Frequency of Occurrence -We can find the weighted frequency of each word by dividing its frequency by the frequency of the most occurring word
# 5)Replace Words by Weighted Frequency in Original Sentences
# 6)Sort Sentences in Descending Order of Sum
  #start:
  # install beAUTIFULL SOAP
  # pip install lxml

import bs4 as bs
import nltk
#nltk.download()
import urllib.request
import re

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Kenya')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)


# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)



sentence_list = nltk.sent_tokenize(article_text)


#Find Weighted Frequency of Occurrence
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1



maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)