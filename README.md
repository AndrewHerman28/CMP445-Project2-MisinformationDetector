# CMP445-Project2-MisinformationDetector
Machine Learning Model to predict a websites credentials and detect misinformation
Link to Web App - https://misinfo-detector-production.up.railway.app/

## About This Project
This project accepts URL links to articles and websites and returns if the content is credible.
This application is meant for anybody in need of confirmation that the source they are reading contains misinformation
This pipeline extracts content from a website, cleans and preprocesses the scraped data, and classifies the credibilty overall. 

## Tech Stack
Languages Used: Python, HTML, JS, CSS
Libraries: pandas, sklearn, joblib, flask, nltk, re, newspaper, urllib

## Intall Code
git clone -----
cd projectname
install all libraries listed above

## How to Use
You can download the merged data directly. If you only have 3 raw data files, run "merge_data.py" to build a clean merged csv.
Run "Predictor.py" once to build the machine learning model and save it as a pickle file in the Models directory
Run "run.py" to run the program and get a locally hosted web app to test the model.

## Project Structure
App/
 ├─ static/
 │   ├─ script.js
 │   └─ style.css
 │
 ├─ templates/
 │   └─ index.html
 │
 ├─ main.py
 ├─ predictor.py
 ├─ preprocessing.py
 ├─ routes.py
 └─ scraper.py

Data/
 ├─ Processed/
 │   └─ merged_data.csv
 │
 ├─ Raw/
 │   ├─ Fake_News_Detection/
 │   │   ├─ Fake.csv
 │   │   └─ True.csv
 │   │
 │   └─ LIAR/
 │       ├─ test.tsv
 │       ├─ train.tsv
 │       └─ valid.tsv
 │
 └─ merge_data.py

Models/
 └─ model/

run.py


# Project Structure
App
  static
    script.js
    style.css
  templates
    index.html
  main.py
  predictor.py
  preprocessing.py
  routes.py
  scraper.py
Data
  Processed
    merged_data.csv
  Raw
    Fake_News_Detection
      Fake.csv
      True.csv
    LIAR
      test.tsv
      train.tsv
      valid.tsv
  merge_data.py
Models
  model
run.py
