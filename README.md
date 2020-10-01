![Django CI](https://github.com/uliang/NaturalLanguageQueryingSystem/workflows/Django%20CI/badge.svg) ![Python 3.8](https://img.shields.io/badge/python-3.8-blue)

# Question and Answering application

## Introduction 

This [Django](https://www.djangoproject.com/) app is a proof of concept of an application that consumes a [spaCy](https://spacy.io/) model to enable users to ask any question regarding some domain and expect an answer.  

This particular application is meant to support questions on salary grades in an organization. Thus one notices that in the `question_answering/models.py` module, the name of the model is `Salary`. 

To customize (or extend) to your particular use, replace (or add) newer Django models. The only requirement is that the table names must correspond to the text categories of the spaCy extension detailed in the next section. 

## Basic requirements of a spaCy extension

This application expects a custom spaCy extension to have been installed. This extension must expose two custom attributes `qtype` and `kb_ident` accessible via the `_` (underscore) attribute of the spaCy document object. 

We assume that the developer has codified knowledge of a particular domain into database tables whose name should correspond to possible `qtype` which the spaCy model has been trained to recognize. 

Rows of each table is identified by `kb_ident`. Therefore the spaCy model powering our system must have been trained to recognize knowledge entities from questions. 

Thus given a question, the spaCy model identifies the question type (`qtype`) and entities (`kb_ident`) from the question and uses this to extract a row from the relevant table. The extracted row is then presented back to the user as the answer. 

At the very minimum, this extension must contain a textcat and custom ner model for it to work. 

Once such extension is installed, set the variable LANG_MODEL to the extension name in the Django settings module. 

```python 
# settings.py

LANG_MODEL='my_spacy_extension'
```
## The `gather_questions` module 

To develop such a question and answering model, one might need to quickly generate questions to bootstrap the process. 

This application exposes the `/gather` endpoint to enable model developers to quickly create a dataset of questions that might be asked in a domain. 

The collection of questions are saved and can be downloaded into spaCy `.jsonl` format. Data can be then annotated and trained to build up the custom model. 

## The main interface 

The index page exposes a simple form where users can enter a question and expect and answer from the model. 

## Deployment 

This application is deployment ready provided the following steps are followed. 

1. Spacy models can be huge. It is suggested that it be hosted on blob storage exposing a URL endpoint. This URL can be added to the requirements.txt file. 

2. Static files should also be hosted on a CDN or seperate static web server. The url should be added to the STATIC_URL environment variable on the host server. 

3. Database credentials and information should be set to the DB_HOST, DB_NAME, DB_USER, DB_PASSWORD and DB_PORT environment variables. 

4. Please set your own unique secret key to the SECRET_KEY environment variable. 
