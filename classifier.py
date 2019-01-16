import glob
import errno
import nltk
import string
import pickle
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
def populate_negative():
  corpus = []
  path = r'C:\Users\daveb_000\Desktop\nets between us\real data\aclImdb\train\neg\*.txt'
  files = glob.glob(path)
  for name in files:
    try:
      with open(name, encoding='utf8') as f:
        content = f.read()
        content = content.split()
        corpus.append(content)
    except IOError as exc:
      if exc.errno != errno.EISDIR:
        raise
  path = r'C:\Users\daveb_000\Desktop\nets between us\real data\aclImdb\test\neg\*.txt'
  files = glob.glob(path)
  for name in files:
    try:
      with open(name, encoding='utf8') as f:
        content = f.read()
        content = content.split()
        corpus.append(content)
    except IOError as exc:
      if exc.errno != errno.EISDIR:
        raise
  bigram_freq = {}
  for text in corpus:
    words = [w.strip(string.punctuation).lower() for w in text]
    for index, word in enumerate(words):
      if index < len(words) - 2:
        w1 = words[index]
        w2 = words[index + 1]
        bigram = (w1, w2)
        if bigram in bigram_freq:
          bigram_freq[bigram] = bigram_freq[bigram] + 1
        else:
          bigram_freq[bigram] = 1
  return bigram_freq
def populate_positive():
  corpus = []
  path = r'C:\Users\daveb_000\Desktop\nets between us\real data\aclImdb\train\pos\*.txt'
  files = glob.glob(path)
  for name in files:
    try:
      with open(name, encoding='utf8') as f:
        content = f.read()
        content = content.split()
        corpus.append(content)
    except IOError as exc:
      if exc.errno != errno.EISDIR:
        raise

  path = r'C:\Users\daveb_000\Desktop\nets between us\real data\aclImdb\test\pos\*.txt'
  files = glob.glob(path)
  for name in files:
    try:
      with open(name, encoding='utf8') as f:
        content = f.read()
        content = content.split()
        corpus.append(content)
    except IOError as exc:
      if exc.errno != errno.EISDIR:
        raise
  bigram_freq = {}
  for text in corpus:
    words = [w.strip(string.punctuation).lower() for w in text]
    for index, word in enumerate(words):
      if index < len(words) - 2:
        w1 = words[index]
        w2 = words[index + 1]
        bigram = (w1, w2)
        if bigram in bigram_freq:
          bigram_freq[bigram] = bigram_freq[bigram] + 1
        else:
          bigram_freq[bigram] = 1
  return bigram_freq

def main():
  corpus = []
  path = r'C:\Users\daveb_000\Desktop\Classes\class_trial.txt'
  files = glob.glob(path)
  for name in files:
    try:
      with open(name) as f:
        content = f.read()
        content = content.split()
        corpus.append(content)
    except IOError as exc:
      if exc.errno != errno.EISDIR:
        raise
  
  with open('neg_bigram', 'rb') as handle:
    neg_bigrams = pickle.load(handle)
  with open('pos_bigram', 'rb') as handle:
    pos_bigrams = pickle.load(handle)
  with open('neg_unigram', 'rb') as handle:
    neg_unigrams = pickle.load(handle)
  with open('pos_unigram', 'rb') as handle:
    pos_unigrams = pickle.load(handle)
  negativity = 0
  positivity = 0
  counter = 0
  sentence_markers = ['.', '?', '!']
  for text in corpus:
    document = []
    for word in text:
      if word[-1] in sentence_markers:
        document.append(word.strip(string.punctuation).lower())
        document.append('END')
      else:
        document.append(word.strip(string.punctuation).lower())
    key = 'film'
    count_neg = 0
    count_pos = 0
    for i in range(len(document) - 2):
      if i == 0:
        if document[i] == key:
          bigram = (document[i+1], document[i+2])
          if bigram in pos_bigrams and bigram in neg_bigrams:
            pos_prob = pos_bigrams[bigram] / ( pos_bigrams[bigram] + neg_bigrams[bigram])
            neg_prob = neg_bigrams[bigram] / ( neg_bigrams[bigram] + pos_bigrams[bigram])
            if neg_prob > pos_prob:
              count_neg += 1
            else:
              count_pos += 1
          elif bigram in pos_bigrams:
            count_pos += 1
          elif bigram in neg_bigrams:
            count_neg += 1
      elif i == 1:
        if document[i] == key:
            bigram = (document[i+1], document[i+2])
            in_front = document[i - 1]
            if bigram in pos_bigrams and bigram in neg_bigrams:
              pos_prob = pos_bigrams[bigram] / ( pos_bigrams[bigram] + neg_bigrams[bigram])
              neg_prob = neg_bigrams[bigram] / ( neg_bigrams[bigram] + pos_bigrams[bigram])
              if neg_prob > pos_prob:
                count_neg += 1
              else:
                count_pos += 1
            elif bigram in pos_bigrams:
              count_pos += 1
            elif bigram in neg_bigrams:
              count_neg += 1
            elif in_front in pos_unigrams and in_front in neg_unigrams:
              pos_prob = pos_unigrams[in_front] / ( pos_unigrams[in_front] + neg_unigrams[in_front])
              neg_prob = neg_unigrams[in_front] / ( neg_unigrams[in_front] + pos_unigrams[in_front])
              if neg_prob > pos_prob:
                count_neg += 1
              else:
                count_pos += 1
            elif in_front in pos_unigrams:
              count_pos += 1
            elif in_front in neg_unigrams:
              count_neg += 1
      else:
        if document[i] == key:
          bigram = (document[i-2],document[i-1])
          bigram2 = (document[i+1],document[i+2])
          in_front = document[i - 1]
          behind = document[i + 1]
          if (bigram in pos_bigrams) and (bigram in neg_bigrams):
            pos_prob = pos_bigrams[bigram] / ( pos_bigrams[bigram] + neg_bigrams[bigram])
            neg_prob = neg_bigrams[bigram] / ( neg_bigrams[bigram] + pos_bigrams[bigram])
            if (bigram2 in pos_bigrams) and (bigram2 in neg_bigrams):
              pos_prob2 = pos_bigrams[bigram2] / ( pos_bigrams[bigram2] + neg_bigrams[bigram2])
              neg_prob2 = neg_bigrams[bigram2] / ( neg_bigrams[bigram2] + pos_bigrams[bigram2])
              counter += 1
              total_pos = (pos_prob * 0.5) + (pos_prob2 * 0.5)
              total_neg = (neg_prob * 0.5) + (neg_prob2 * 0.5)
              if total_pos > total_neg:
                count_pos += 1
              else:
                count_neg += 1
            elif bigram2 in pos_bigrams:
              if pos_prob > neg_prob:
                count_pos += 1
            elif bigram2 in neg_bigrams:
              if neg_prob > pos_prob:
                count_neg += 1
            else:
              if pos_prob > neg_prob:
                count_pos += 1
              else:
                count_neg += 1  
          elif bigram in pos_bigrams:
            if bigram2 in pos_bigrams and bigram2 in neg_bigrams:
              pos_prob2 = pos_bigrams[bigram2] / ( pos_bigrams[bigram2] + neg_bigrams[bigram2])
              neg_prob2 = neg_bigrams[bigram2] / ( neg_bigrams[bigram2] + pos_bigrams[bigram2])
              if pos_prob2 > neg_prob2:
                count_pos += 1
            elif bigram2 not in neg_bigrams:
              count_pos += 1
          elif bigram in neg_bigrams:
            if bigram2 in pos_bigrams and bigram2 in neg_bigrams:
              pos_prob2 = pos_bigrams[bigram2] / ( pos_bigrams[bigram2] + neg_bigrams[bigram2])
              neg_prob2 = neg_bigrams[bigram2] / ( neg_bigrams[bigram2] + pos_bigrams[bigram2])
              if pos_prob2 < neg_prob2:
                count_neg += 1
            elif bigram2 not in pos_bigrams:
              count_neg += 1
          elif bigram2 in pos_bigrams and bigram2 in neg_bigrams:
            pos_prob2 = pos_bigrams[bigram2] / ( pos_bigrams[bigram2] + neg_bigrams[bigram2])
            neg_prob2 = neg_bigrams[bigram2] / ( neg_bigrams[bigram2] + pos_bigrams[bigram2])
            if pos_prob2 > neg_prob2:
              count_pos += 1
            else:
              count_neg += 1
          elif bigram2 in pos_bigrams:
            count_pos += 1
          elif bigram2 in neg_bigrams:
            count_neg += 1
          elif in_front in pos_unigrams and in_front in neg_unigrams:
            prob_pos = pos_unigrams[in_front] / ( pos_unigrams[in_front] + neg_unigrams[in_front])
            prob_neg = neg_unigrams[in_front] / ( neg_unigrams[in_front] + pos_unigrams[in_front])
            if prob_neg > 0.744:
              count_neg += 1
            if prob_pos > 0.744:
              count_pos += 1
          elif in_front in neg_unigrams:
            count_neg += 1
          elif in_front in pos_unigrams:
            count_pos += 1
            
#    print(text[0], text[-1], count_pos, 'count pos')
#    print(text[0], text[-1], count_neg, 'count_neg')
    if count_neg < count_pos:
      positivity = positivity + (count_pos - count_neg)
    else:
      negativity = negativity + (count_neg - count_pos)
  if positivity > negativity:
    print('Positive')
  else:
    print('Negative')
  print(positivity)
  print(negativity)
  print(key)
main()
