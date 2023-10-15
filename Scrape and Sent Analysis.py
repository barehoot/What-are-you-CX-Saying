#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 23:58:16 2023

@author: pradhyumnsingh
"""

import re
import os
import nltk
import pandas as pd
from newspaper import Article
from nltk.corpus import words
nltk.download("words")
nltk.download("punkt")

# Constants
DIRECTORY_PATH = "/Users/pradhyumnsingh/Desktop/Submission Blackcoffer"
POSITIVE_WORDS_FILE = "/Users/pradhyumnsingh/Desktop/MasterDictionary/positive-words.txt"
NEGATIVE_WORDS_FILE = "/Users/pradhyumnsingh/Desktop/MasterDictionary/negative-words.txt"

def count_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return len(sentences)

def count_syllables(word):
 
  # Split the word into syllables.
  syllables = nltk.word_tokenize(word)

  # Count the number of syllables.
  syllable_count = 0
  for syllable in syllables:
    if syllable:
      syllable_count += 1

  return syllable_count

def calculate_average_words_per_sentence(text):

    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Count the number of words in each sentence
    word_counts = [len(nltk.word_tokenize(sentence)) for sentence in sentences]

    # Calculate the total number of words
    total_word_count = sum(word_counts)

    # Calculate the number of sentences
    number_of_sentences = len(sentences)

    # Calculate the average number of words per sentence
    average_words_per_sentence = total_word_count / number_of_sentences

    return average_words_per_sentence

def calculate_average_word_length(text):
    # Split the text into words
    words = nltk.word_tokenize(text)

    # Count the number of characters in each word
    character_counts = [len(word) for word in words]

    # Calculate the total number of characters
    total_character_count = sum(character_counts)

    # Calculate the number of words
    number_of_words = len(words)

    # Calculate the average word length
    average_word_length = total_character_count / number_of_words

    return average_word_length


def count_complex_words(text):
    word_tokens = nltk.word_tokenize(text)
    word_set = set(words.words())
    complex_word_count = sum(1 for word in word_tokens if word.lower() not in word_set)
    return complex_word_count

def count_personal_pronouns(text):
    personal_pronoun_regex = re.compile(r'\b(?:I|we|my|ours|us)\b', flags=re.IGNORECASE)
    return len(personal_pronoun_regex.findall(text))

def analyze_sentiment(file_name, pos_words, neg_words, stopwords):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()

        # Remove custom stop words from the file content
        words = re.findall(r'\w+', content)
        total_word_count = len(words)
        filtered_words = [word for word in words if word.lower() not in stopwords]
        filtered_word_count = len(filtered_words)

        positive_score = sum(1 for word in filtered_words if word.lower() in pos_words)
        negative_score = sum(1 for word in filtered_words if word.lower() in neg_words)
        polarity = (positive_score - negative_score) / (positive_score + negative_score + 1e-6)
        subjectivity = abs(positive_score - negative_score) / (filtered_word_count + 1e-6)
        avg_sentence_length = total_word_count / count_sentences(content)
        complex_word_count = count_complex_words(content)
        percentage_complex_words = (complex_word_count / filtered_word_count) * 100
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
        total_char_count = sum(len(word) for word in words)
        avg_word_length = total_char_count / filtered_word_count
        syllables_per_word = count_syllables(content)
        avg_wordper_sentence= calculate_average_words_per_sentence(content)
        personal_pronoun_count = count_personal_pronouns(content)
        average_word_length = calculate_average_word_length(content)

        return positive_score, negative_score, polarity, subjectivity, avg_sentence_length, percentage_complex_words, fog_index,avg_wordper_sentence , avg_word_length, complex_word_count,syllables_per_word, personal_pronoun_count, average_word_length

    except Exception as e:
        print(f"An error occurred while analyzing {file_name}: {str(e)}")
        return None, None, None, None, None, None, None, None, None, None, None, None, None

def main():
    # Load the list of positive words
    with open(POSITIVE_WORDS_FILE, "r", encoding="utf-8") as pos_file:
        pos_words = pos_file.read().splitlines()

    # Load the list of negative words
    with open(NEGATIVE_WORDS_FILE, "r", encoding="latin-1") as neg_file:
        neg_words = neg_file.read().splitlines()

    # Load custom stop words
    custom_stopwords_file = "/Users/pradhyumnsingh/Desktop/StopWords"
    custom_stopwords = set()
    for file_name in os.listdir(custom_stopwords_file):
        with open(os.path.join(custom_stopwords_file, file_name), "r", encoding="latin-1") as stopwords_file:
            custom_stopwords.update(stopwords_file.read().splitlines())

    # Read the Excel file and extract URLs
    excel_file_path = "/Users/pradhyumnsingh/Desktop/Submission Blackcoffer/Input.xlsx"
    df = pd.read_excel(excel_file_path)

    # Create a DataFrame to store the sentiment analysis results
    data = []

    for index, row in df.iterrows():
        url = row['URL']  # Assuming the column name in Excel is 'URL'
        url_id = row['URL_ID']
        try:
            # Initialize Article object
            article = Article(url)

            # Download and parse the article
            article.download()
            article.parse()

            # Generate a file name from the URL
            file_name = os.path.join(DIRECTORY_PATH, url.replace("/", "_") + ".txt")

            # Save the article content to a text file
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(f"Title: {article.title}\n\n")
                file.write(article.text)

            print(f"Article from URL {url} saved to {file_name}")

            # Perform sentiment analysis for the current URL
            positive, negative, polarity, subjectivity, avg_sln, pct_compl_words, fog_index,avgwpsen , avg_word_len, compl_word_count, SylCount, pronoun_count, awlen = analyze_sentiment(
                file_name, pos_words, neg_words, custom_stopwords)
            if positive is not None and negative is not None and polarity is not None and subjectivity is not None:
                data.append([url_id, url, positive, negative, polarity, subjectivity, avg_sln, pct_compl_words, fog_index,avgwpsen , avg_word_len, compl_word_count,SylCount , pronoun_count, awlen])

        except Exception as e:
            print(f"An error occurred while processing URL {url}: {str(e)}")

    # Create a DataFrame with columns for URL, Polarity, and Subjectivity
    df2 = pd.DataFrame(data, columns=["URL_ID", "URL", "Positive Words", "Negative Words", "Polarity", "Subjectivity", "Average Sentence Length", "Percent of Complicated Word", "Fog Index","Average Words per Sentence" , "Average Word Length", "Complex Word Count","Syllable count per word" , "Personal Pronoun Count", "Average Word Length"])

    # Save the sentiment analysis results to an Excel file
    excel_file_path = "sentiment_analysis_Pr.xlsx"
    df2.to_excel(excel_file_path, index=False)
    print(f"Sentiment analysis results saved to {excel_file_path}")

if __name__ == "__main__":
    main()
