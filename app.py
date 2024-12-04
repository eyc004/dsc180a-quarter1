import streamlit as st 
import os
import requests, uuid, json
import guardrails as gd
from guardrails import Guard, OnFailAction
from guardrails.hub import SensitiveTopic


# For the user to switch to their own API keys
os.environ["OPENAI_API_KEY"] = "<YOUR OPENAI API KEY>"
key = "<YOUR MICROSOFT AZURE AI KEY>"

endpoint = "https://api.cognitive.microsofttranslator.com"
location = "westus2"
path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['zh-Hans']
}

# Using Guardrails AI SensitiveTopic Guardrail to not translate anything political
guard = Guard().use(
    SensitiveTopic,
    sensitive_topics=["politics"],
    disable_classifier=True,
    disable_llm=False,
    on_fail="exception",
    llm_callable="gpt-3.5-turbo"
)


# Function to translate English into Simplified Chinese using Microsoft's Translation Services
def without_guardrails(input_text):  
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': input_text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translation_text = response[0]['translations'][0]['text']
    return translation_text

# The function to create the Streamlit app    
def main():
    st.title("Guardrail Implementation in LLMs")
    text_area = st.text_area("Enter the English text you want to translate into Simplified Chinese!")

    if st.button("Translate"):
        if len(text_area) > 0:
            st.info(text_area)

            # Does the translation first without guardrails
            st.warning("Translation Without Guardrails")
            without_guardrails_result = without_guardrails(text_area)
            st.success(without_guardrails_result)

            st.info("Translation With Guardrails")
            # Then tries the translation with the SensitiveTopic Guardrail
            try: 
                validated_input = guard.validate(text_area)
                # If the guardrail validates the input text, then act like it's as if there are no guardrails
                st.success(without_guardrails_result)
            except Exception as e:
                st.write(e)

if __name__ == '__main__':
    main()
