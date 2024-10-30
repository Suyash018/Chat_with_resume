# Project overview

IMPORTANT: This is an assignment for hostmegrow. I donot Authorize cloneing or Forking this repo by any candidate taking part in the recruitment process of hostmegrow.

This project consists of two Parts:
1. Resume Summarizer - Summarizes Resume as required by the Assesignment
2. Chat with resume - Helps you to chat with info regarding the resume.I have restricted the chatbot.

It is streamlit app as I am not that good with webdev. I Can implement FAST API / FLASK API I personally prefer FAST API due to its ease of use and faster response time.

Deployed in Streamlit online: [https://chatwithresume-jotkl3tnspds8zewdurjfc.streamlit.app/](https://chatwithresume-jotkl3tnspds8zewdurjfc.streamlit.app/) 
- No need for env keys as it is in Secret of the streamlit application.

## Offline Setup instructions

- Make an file called .env
```txt
OPENAI_API_KEY="Your-env-key"
```

- Clone the Repo
- Install the requirements using

```python
pip install -r requirements.txt
```
## How to run the application

```python
streamlit run app.py
```

## Where to place API keys
- Make an file called .env
```txt
OPENAI_API_KEY="Your-env-key"
```
## Any assumptions or limitations
- All the assumptions are handleld by error Handling

## Future improvements
- Convert to fast API with better UI
- Support for image file like .png,.jpeg,.jpg
- Support for multiple resume upload.
    - Save all output to csv.
    - Add Filtering Option to find best candidate for future Hiring using it.
    - Suggest resume that best fit the current requirements.
    - Send Automated mail to selected resume.