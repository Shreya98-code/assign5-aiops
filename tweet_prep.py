# -*- coding: utf-8 -*-
"""
Created on Sat Feb  29 20:30:26 2020

@author: Shreya_agrawal
"""

"""
Assignment 5: Preprocessor Library
"""

from nl_stuff import TweetTokenizer
import re

class Preprocessor:
    """
    Pre processing text to generate padded embeddings of tweet
    """
    def __init__(self, pad_length_tweet = 50, max_length_dictionary=100000):

        """
        Initializing class
        :parameters pad_length_tweet:
        :parameters max_length_dictionary:
        :parameters embeddings_dict:
        :parameters file_path
        """

        self.pad_length_tweet = pad_length_tweet
        self.max_length_dictionary = max_length_dictionary
        self.embeddings = []
        
        #print("Inside init")

        #Loading the list
        count = 0
        with open("word_list.txt") as file:
            for line in file:
                values = line.split('\n')
                word = values[0]
                self.embeddings.append(word)
                count += 1
                if count > max_length_dictionary:
                    break
                
        
        #print(self.embeddings[0])
                        

        self.tokenizer = TweetTokenizer()
     
    @staticmethod
    def stop_words_remove(tweet):
        """
        Separate method to remove stopwords
        """
        
        # importing stopwords directly as a list
        stopwords = []
        with open("english") as files:
            for line in files:
                values = line.split('\n')
                word = values[0]
                stopwords.append(word)

        
        patt = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
        tweet = patt.sub('', tweet)
        return tweet

    def clean(self, tweet):
        """
        Cleaning text
        """

        # URL
        tweet = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", '', tweet)

        tweet = tweet.lower()

        # Numbers
        tweet = re.sub(r"[0-9]+", '', tweet)

        # Stopwords
        tweet = self.stop_words_remove(tweet)

        # Removing #
        tweet = re.sub(r"#", '', tweet)

        # Removing handles
        tweet = re.sub(r"@[a-zA-Z0-9]+", '', tweet)

        return tweet

    def tokenize_text(self, tweet):

        """
        Tokenizing tweet
        """
        tokenized = self.tokenizer.tokenize(tweet)
        
        return tokenized

    def replace_with_index(self, token_list):
        """
        Replace token with embeddings index
        """
        list_of_index = []
        for token in token_list:
            try:
                token_index = self.embeddings.index(token)
                list_of_index.append(token_index)
            except ValueError:
                embed = self.embeddings.index('<unknown>')
                list_of_index.append(embed)
        return list_of_index

    def pad_sequence(self, index_list):
        """
        Pad tokenized sequence
        """
        length1 = len(index_list)

        if length1 < self.pad_length_tweet:
            req_d = self.pad_length_tweet - length1
            pad = [self.embeddings.index('<pad>')]
            index_list.extend(pad*req_d)
            token_padded = index_list

        elif length1 == self.pad_length_tweet:
            token_padded = index_list

        else:
            token_padded = index_list[:self.pad_length_tweet]

        return token_padded

    def tweet_process(self, tweet):

        """
        complete end to end function
        """

        cleaned = self.clean(tweet)
        tokenized = self.tokenize_text(cleaned)
        token_index = self.replace_with_index(tokenized)
        padded_index = self.pad_sequence(token_index)
        
        print("Inside")

        return padded_index



#sample = "I am doing absolutely fine"
#Twitter = Preprocessor()
#print Twitter.tweet_process(sample)
