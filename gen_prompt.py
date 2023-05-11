import openai
from rlsapp import rlsapp, collection

openai.api_key = "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"

def get_chat_response(prompt):
    model_engine = "davinci"  # you can choose a different model here if you'd like
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

rlsno = '3974265'
client = collection.find_one({'rlsno': rlsno})

prompt = "Draft grounds for applying for asylum on the basis of " + client['reasons'][0] + " arising from the fact that the applicant " + client['basis'] 

print(prompt)

#chat_response = get_chat_response(prompt)
#quoted_response = f'"{chat_response}"'
#print(quoted_response)

