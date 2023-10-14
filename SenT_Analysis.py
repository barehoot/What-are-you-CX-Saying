#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:44:28 2023

@author: pradhyumnsingh
"""

import re
from newspaper import Article
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import os
import pandas as pd
from nltk.corpus import words
nltk.download("words")
nltk.download("punkt")

nltk.download('stopwords')

def count_complex_words(text):
    word_tokens = nltk.word_tokenize(text)
    word_set = set(words.words())
    complex_word_count = sum(1 for word in word_tokens if word.lower() not in word_set)
    return complex_word_count

def count_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return len(sentences)

def count_personal_pronouns(text):
    personal_pronoun_regex = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)
    return len(personal_pronoun_regex.findall(text))

def count_syllables(word):
 
  # Split the word into syllables.
  syllables = nltk.word_tokenize(word)

  # Count the number of syllables.
  syllable_count = 0
  for syllable in syllables:
    if syllable:
      syllable_count += 1

  return syllable_count



def save_article_with_sentiment_analysis(url, pos_words, neg_words):
    try:
        # Initialize Article object
        article = Article(url)
        
        # Download and parse the article
        article.download()
        article.parse()

        # Generate a file name from the URL
        file_name = url.replace("://", "_").replace("/", "_") + ".txt"

        # Remove stopwords from the article text
        stop_words = set(stopwords.words("english"))
        text = article.text
        words = re.findall(r'\w+', text)
        filtered_text = " ".join([word for word in words if word.lower() not in stop_words])
        filtered_word_count= len(filtered_text)

        # Perform sentiment analysis using TextBlob
        sentiment = TextBlob(filtered_text)
        sentiment_polarity = sentiment.sentiment.polarity
        sentiment_subjectivity = sentiment.sentiment.subjectivity
        positive_score = sum(1 for word in filtered_text if word.lower() in pos_words)
        negative_score = sum(1 for word in filtered_text if word.lower() in neg_words)
        avg_sentence_length = filtered_word_count / count_sentences(filtered_text)
        complex_word_count = count_complex_words(filtered_text)
        percentage_complex_words = (complex_word_count / filtered_word_count) * 100
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
       # total_char_count = sum(len(word) for word in words)
        #avg_word_length = total_char_count / filtered_word_count
        syllables_per_word = count_syllables(filtered_text)
        personal_pronoun_count = count_personal_pronouns(filtered_text)

        # Save the article content without stop words and sentiment analysis results to a text file
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"Title: {article.title}\n\n")
            file.write(f"Text (without stop words):\n{filtered_text}\n\n")
            file.write(f"Sentiment Polarity: {sentiment_polarity}\n")
            file.write(f"Sentiment Subjectivity: {sentiment_subjectivity}\n")
            
        print(f"Article saved to {file_name} with sentiment analysis results")
        
        return sentiment, sentiment_polarity, sentiment_subjectivity, positive_score, negative_score, avg_sentence_length, complex_word_count, percentage_complex_words,fog_index, syllables_per_word, personal_pronoun_count

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    url = input("Enter the URL of the article: ")
    
    POSITIVE_WORDS_FILE = "/Users/pradhyumnsingh/Desktop/MasterDictionary/positive-words.txt"
    NEGATIVE_WORDS_FILE = "/Users/pradhyumnsingh/Desktop/MasterDictionary/negative-words.txt"

    with open(POSITIVE_WORDS_FILE, "r", encoding="utf-8") as pos_file:
        pos_words = pos_file.read().splitlines()

    # Load the list of negative words
    with open(NEGATIVE_WORDS_FILE, "r", encoding="latin-1") as neg_file:
        neg_words = neg_file.read().splitlines()
        
        data=[]
        
        sentiment, sentiment_pol, Sentiment_sub,positive, negative, avg_sln,compl_word_count, pct_compl_words, fog_index , SylCount, pronoun_count = save_article_with_sentiment_analysis(
            url, pos_words, neg_words)
        if positive is not None and negative is not None:
            data.append([url,sentiment, sentiment_pol, Sentiment_sub, positive, negative, avg_sln, compl_word_count, pct_compl_words, fog_index, SylCount , pronoun_count])
  # Create a DataFrame with columns for URL, Polarity, and Subjectivity
    df2 = pd.DataFrame(data, columns=[ "URL","Sentiment","Sentiment Polarity","Sentiment subjectivity", "Positive Words", "Negative Words", "Average Sentence Length", "Percent of Complicated Word", "Fog Index", "Average Word Length","Syllable count per word" , "Personal Pronoun Count"])

  # Save the sentiment analysis results to an Excel file
    excel_file_path = "sentiment_analys.xlsx"
    df2.to_excel(excel_file_path, index=False)
    print(f"Sentiment analysis results saved to {excel_file_path}")
