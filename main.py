from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
import nltk
import io
import PyPDF2 as ppf
import pandas as pd
import re

app = Flask(__name__)

def get_content_from_pdf(url):
   text_string = ""
   req_obj = requests.get(url)
   f = io.BytesIO(req_obj.content)
   reader = ppf.PdfFileReader(f)
   for i in range(reader.numPages):
    current_page = reader.getPage(i)
    extracted_text = current_page.extractText()
    text_string = text_string + extracted_text
   return text_string

def get_wiki_content(url):
   req_obj = requests.get(url)
   text = req_obj.text
   soup = BeautifulSoup(text)
   all_paras = soup.find_all("p")
   wiki_text = ''
   for para in all_paras:
      wiki_text += para.text 
   return wiki_text



def top10_sent(url):
    if '.pdf' in url:
        og_text = get_content_from_pdf(url)
    else:
        og_text = get_wiki_content(url)
    stopwords = nltk.corpus.stopwords.words("english")
    sentences = nltk.sent_tokenize(og_text)
    words = nltk.word_tokenize(og_text)
    word_freq = {}
    for word in words:
        if word not in stopwords:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    
    max_word_freq = max(word_freq.values())
    for key in word_freq.keys():
        word_freq[key] /= max_word_freq
    
    sentences_score = []
    for sent in sentences:
        curr_words = nltk.word_tokenize(sent)
        curr_score = 0
        for word in curr_words:
            if word in word_freq:
                curr_score += word_freq[word]
        sentences_score.append(curr_score)

    sentences_data = pd.DataFrame({"sent":sentences, "score":sentences_score})
    sorted_data = sentences_data.sort_values(by = "score", ascending = False).reset_index()

    get_summary = sorted_data.iloc[0:11,:]
    
    #top_10 = list(sentences_data.sort_values(by = "score",ascending = False).reset_index().iloc[0:11,"sentences"])
    return (" ".join(list(get_summary["sent"])), og_text)

def remove_citation(summary_doc):
    text_after_removing_citation = re.sub("[\[].*?[\]]", '', summary_doc)
    summary_after_removing_citation = text_after_removing_citation.strip()
    return summary_after_removing_citation
    

@app.route("/", methods = ["GET", "POST"])
def index():
   if request.method == "POST":
      url = request.form["url"]
      url_content = top10_sent(url)
      content_for_removing_citations = url_content[0]
      summary_without_citation = remove_citation(content_for_removing_citations)
      return render_template("result.html",final_summary = summary_without_citation, original_text = url_content[1])
   return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

    