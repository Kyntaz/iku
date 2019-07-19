import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import random

class SeasonClassifier:
    def __init__(self):
        self.summer_words = ['summer', 'hot', 'sun', 'desert', 'fire']
        self.spring_words = ['spring', 'growth', 'flower', 'air', 'love']
        self.autumn_words = ['autumn', 'leaf', 'decay', 'earth', 'nostalgia']
        self.winter_words = ['winter', 'snow', 'water', 'death', 'cold']
        self.train_set = []
        self.classifier = None
        
    def init_words(self):
        with open('texts\\summer.txt', 'r', encoding='utf8') as f:
            for t in f:
                self.summer_words += word_tokenize(t)
        with open('texts\\spring.txt', 'r', encoding='utf8') as f:
            for t in f:
                self.spring_words += word_tokenize(t)
        with open('texts\\autumn.txt', 'r', encoding='utf8') as f:
            for t in f:
                self.autumn_words += word_tokenize(t)
        with open('texts\\winter.txt', 'r', encoding='utf8') as f:
            for t in f:
                self.winter_words += word_tokenize(t) 
               
        stopWords = set(stopwords.words('english')) 
        self.summer_words = list(set(filter(lambda w: not (w in stopWords or re.match(r'[A-Za-z]', w) == None), self.summer_words)))
        self.spring_words = list(set(filter(lambda w: not (w in stopWords or re.match(r'[A-Za-z]', w) == None), self.spring_words)))
        self.winter_words = list(set(filter(lambda w: not (w in stopWords or re.match(r'[A-Za-z]', w) == None), self.winter_words)))
        self.autumn_words = list(set(filter(lambda w: not (w in stopWords or re.match(r'[A-Za-z]', w) == None), self.autumn_words)))
        
        self.summer_words = list(set(filter(lambda w: not w in self.spring_words + self.winter_words + self.autumn_words, self.summer_words)))
        self.spring_words = list(set(filter(lambda w: not w in self.summer_words + self.winter_words + self.autumn_words, self.spring_words)))
        self.winter_words = list(set(filter(lambda w: not w in self.spring_words + self.summer_words + self.autumn_words, self.winter_words)))
        self.autumn_words = list(set(filter(lambda w: not w in self.spring_words + self.winter_words + self.summer_words, self.autumn_words)))
        
        random.shuffle(self.summer_words)
        random.shuffle(self.winter_words)
        random.shuffle(self.spring_words)
        random.shuffle(self.autumn_words)
        s = min(len(self.summer_words), len(self.winter_words), len(self.spring_words), len(self.autumn_words))
        self.summer_words = self.summer_words[:s]
        self.winter_words = self.winter_words[:s]
        self.spring_words = self.spring_words[:s]
        self.autumn_words = self.autumn_words[:s]

    def init_train_set(self):
        summer_feats = [(word_feats(w), 'summer') for w in self.summer_words]
        spring_feats = [(word_feats(w), 'spring') for w in self.spring_words]
        autumn_feats = [(word_feats(w), 'autumn') for w in self.autumn_words]
        winter_feats = [(word_feats(w), 'winter') for w in self.winter_words]
        self.train_set = summer_feats + spring_feats + winter_feats + autumn_feats
        
    def init_classifier(self):
        self.init_train_set()
        self.classifier = NaiveBayesClassifier.train(self.train_set)
        
    def classify_word(self, word):
        return self.classifier.classify(word_feats(word))
    
    def classify_verse(self, verse):
        words = word_tokenize(verse)
        stopWords = set(stopwords.words('english'))
        words = list(filter(lambda w: not w in stopWords, words))
        
        su = 0
        wi = 0
        au = 0
        sp = 0
        for word in words:
            if re.match(r'[A-Za-z]', word) == None: continue
            if word in self.summer_words: su = su + 2
            if word in self.winter_words: wi = wi + 2
            if word in self.autumn_words: au = au + 2
            if word in self.spring_words: sp = sp + 2
            
            cl = self.classify_word(word)
            if cl == 'summer': su = su + 1
            if cl == 'winter': wi = wi + 1
            if cl == 'autumn': au = au + 1
            if cl == 'spring': sp = sp + 1
        if max(su, wi, au, sp) == su: return 'summer'
        if max(su, wi, au, sp) == wi: return 'winter'
        if max(su, wi, au, sp) == au: return 'autumn'
        if max(su, wi, au, sp) == sp: return 'spring'

def word_feats(word):
    return dict([(l, True) for l in word])