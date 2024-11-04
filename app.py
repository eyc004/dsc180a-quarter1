import streamlit as st 
from dotenv import load_dotenv
import requests, uuid, json
import guardrails as gd
from guardrails import Guard, OnFailAction
from guardrails.hub import CompetitorCheck



load_dotenv()

key = "INSERT YOUR API KEY HERE"
endpoint = "https://api.cognitive.microsofttranslator.com"


location = "westus2"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'zh-Hans',
    'to': ['en']
}

# Basic Election and Geopolitical Red Flags
guard = Guard().use(
    CompetitorCheck, ["Trump", "Harris", "Donald Trump", "Kamala Harris", "United States", "China"], "exception"
)

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

    
def main():
    st.title("Guardrail Implementation in LLMs")
    text_area = st.text_area("Enter the Simplified Chinese text you want to translate into English!")

    if st.button("Translate"):
        if len(text_area) > 0:
            st.info(text_area)
        
            st.warning("Translation Without Guardrails")
            without_guardrails_result = without_guardrails(text_area)
            st.success(without_guardrails_result)

            st.info("Translation With Guardrails")
            try: 
                validated_translation = guard.validate(without_guardrails_result)
                st.success(validated_translation.validated_output)
            except Exception as e:
                st.write(e)

if __name__ == '__main__':
    main()
