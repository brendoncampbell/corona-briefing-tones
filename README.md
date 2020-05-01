# corona-briefing-tones

![alt text](imgs/trump_task_force.jpg)
President Donald Trump speaking during a press briefing with the coronavirus task force on March 19, 2020. (AP Photo/Evan Vucci)

###  DRAFT OUTLINE

1. `eda_cleaning.ipynb`
    - Calls `src/scrape_briefings.py` to retrieve briefing corpus
    - Exports transcripts as cleaned csv 

2. `sentiment_emotion_scores.ipynb`
    - Reads in cleaned corpus csv
    - TextBlob & Vader sentiment analysis 
    - Emotion scoring using NRC's open source emotion lexicon
    - Exports csv with sentiment and emotion scores

3. `topic_modelling.ipynb`
    - Reads in csv exported from sentiment/emotion analysis
    - LDA model to derive and assign topics to each piece of text
    - Exports csv with topic assignments

4. `analysis.ipynb`
    - Initial visualization and exploration of emotions and topics

