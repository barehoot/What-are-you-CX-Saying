# What-are-you-CX-Saying

**Instructions for Using Sentiment Analysis Script**

This script is designed to perform sentiment analysis on a list of URLs. It extracts content from the provided URLs using the Newspaper library and analyzes the sentiment of the extracted articles. Follow the steps below to use the script:

**Prerequisites:**

1. Python 3.x installed on your system.
2. The required Python libraries must be installed. You can install them using `pip`:
   - `newspaper3k`
   - `nltk`
   - `pandas`

   To install these libraries, open a command prompt and run:
   ```
   pip install newspaper3k nltk pandas
   ```

**Configuration:**

1. Make sure you have the following files and directories set up:
   - The script itself.
   - A directory where you want to save the extracted articles (set in `DIRECTORY_PATH`).
   - Text files containing positive and negative words for sentiment analysis (set in `POSITIVE_WORDS_FILE` and `NEGATIVE_WORDS_FILE`).
   - A directory with custom stop words (set in `custom_stopwords_file`).

**Steps:**

1. Place your Excel file containing the list of URLs in the same directory as the script. Make sure the Excel file has the following columns:
   - 'URL': This column should contain the URLs to the articles you want to analyze.
   - 'URL_ID': This column should contain unique identifiers for each URL.

2. Open the script file in a text editor or Python IDE.

3. Update the following variables in the script to match your file paths and settings:
   - `DIRECTORY_PATH`: Set the path where you want to save the extracted articles.
   - `POSITIVE_WORDS_FILE`: Set the path to the file containing positive words.
   - `NEGATIVE_WORDS_FILE`: Set the path to the file containing negative words.
   - `custom_stopwords_file`: Set the path to the directory containing custom stop words.

4. Save your changes in the script.

5. Open a command prompt or terminal.

6. Navigate to the directory containing the script and the Excel file.

7. Run the script using the following command:
   ```
   python script_name.py
   ```

   Replace `script_name.py` with the actual name of your Python script.

8. The script will start processing each URL, saving the articles to text files and performing sentiment analysis.

9. After processing all URLs, the sentiment analysis results will be saved in an Excel file named "sentiment_analysis_Pr.xlsx" in the same directory as the script.

10. You can review the sentiment analysis results in the Excel file.

**Notes:**

- Ensure that you have the necessary permissions to read and write files in the specified directories.

These instructions provide an overview of how to use the script. If you encounter any issues or have specific requirements, you may need to adjust the script accordingly.
