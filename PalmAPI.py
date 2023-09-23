import pprint
import google.generativeai as palm
import json

palm.configure(api_key="API_Key")
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)


def get_chat_response(user_text):
    prompt = """
You are an expert at legal documentations. Understand the key attributes mentioned in the prompt and return them as key value pairs in python dictionary. Use indian
Standards in all scenarios.

Generate a Leese agreement for the following scenario:


"""
    prompt=prompt+"\n"+user_text
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=1500,
        )

    return completion.result

