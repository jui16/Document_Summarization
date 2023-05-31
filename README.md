# Document_Summarization

Thsi project aims towards summarizing a given document using Python's nltk library.
input = a link to the doccument
output = summarized text


# *Abstract*: 
Text summarization is a technique for generating the summary from the lengthy documents. The main aim of this technique is to provide the summary while focusing on the sections that convey important information. Automatic text summarization is helpful for transferring documents into shortened versions, which is time consuming if done manually. Document summarization systems are generally based on the technology called ‘Natural Language Processing’. In this academic mini project we aim to build the text summarizer using TextRank Algorithm.

# *Detailed Explanation / Steps*: 
The first step would be to concatenate all the text contained in the articles
Then split the text into individual sentences
Text preprocessing - Word tokenization, stopword removal
In the next step, we will find vector representation (word embeddings) for each and every sentence
Similarities between sentence vectors are then calculated and stored in a matrix
The similarity matrix is then converted into a graph, with sentences as vertices and similarity scores as edges, for sentence rank calculation
Finally, a certain number of top-ranked sentences form the final summary.

# *Tech-Stack*:
NLTK
Beautiful Soup
TF-IDF Model
HTML, CSS
Flask
PyPDF2
Pandas



