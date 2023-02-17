from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# from helper.openai_api import text_complition


app = Flask(__name__)

@app.route('/dialogflow/cx/receiveMessage', methods=['POST'])
def cxReceiveMessage():
    try:
        data = request.get_json()
        # Use this tag peoperty to choose the action
        # tag = data['fulfillmentInfo']['tag']
        query_text = data['text']
        print(query_text)
        result = text_complition(query_text)
        print(result)
        print(result['response'])
        if result['status'] == 1:
            return jsonify(
                {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [result['response']],
                                    'redactedText': [result['response']]
                                },
                                'responseType': 'HANDLER_PROMPT',
                                'source': 'VIRTUAL_AGENT'
                            }
                        ]
                    }
                }
            )
    except Exception as e:
        print(e)
        pass
    return jsonify(
        {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': ['Something went wrong.'],
                            'redactedText': ['Something went wrong.']
                        },
                        'responseType': 'HANDLER_PROMPT',
                        'source': 'VIRTUAL_AGENT'
                    }
                ]
            }
        }
    )
def text_complition(prompt: str) -> dict:
    '''
    Call Openai API for text completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=f'Human: {prompt}\nAI: ',
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=['Human:', 'AI:']
        )
        return {
            'status': 1,
            'response': response['choices'][0]['text']
        }
    except Exception as e:
        print(e)
        return {
            'status': 0,
            'response': ''
        }
 
if __name__ == '__main__':
    app.run(debug=True)
    