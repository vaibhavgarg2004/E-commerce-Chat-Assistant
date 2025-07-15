import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq()

def talk(query):
    prompt = f'''You are a helpful and friendly e-commerce chatbot. Besides answering FAQs and suggesting products, you can engage in light small talk to make the shopping experience more pleasant. Keep your responses concise—no more than two lines—and stay relevant to your role as a shopping assistant.

    QUESTION: {query}
    '''
    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    query = "How are you?"
    answer = talk(query)
    print("Answer:",answer)