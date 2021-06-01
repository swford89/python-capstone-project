from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

# function to create API client object
def create_ibm_api():
    # fetch virtual environment variables
    IAM_IDENTITY_KEY = os.environ['IAM_IDENTITY_KEY']
    URL = os.environ['URL']

    # authenticate
    authenticator = IAMAuthenticator(IAM_IDENTITY_KEY)
    tone_analyzer = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
    end_point = tone_analyzer.set_service_url(URL)
    return tone_analyzer, end_point

# function to analyze text and format the data for entry into DB
def tone_data(tone_analyzer, text):
    tone_analysis = tone_analyzer.tone({'text': text}).get_result()
    tweet_tones = []
    try:
        for tone in tone_analysis['document_tone']['tones']:
            found_tone = f"{tone['tone_name']}: {tone['score'] * 100:.2f}%"
            tweet_tones.append(found_tone)
    except IndexError:
        tweet_tones = 'INCONCLUSIVE'
    return str(tweet_tones)