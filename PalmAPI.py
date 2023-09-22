import pprint
import google.generativeai as palm
palm.configure(api_key="AIzaSyAgL6CKRbjUaJ52mS_vJx9Fn7k87tIG93U")
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)
prompt = """
You are an expert at legal documentations. Understand the key attributes mentioned in the prompt and return them as key value pairs in python dictionary. Use indian
Standards in all scenarios.

Generate a Leese agreement for the following scenario:

Lessor Kartik Goyal is leesing his 2 storied house of 540 acres at Marina Bay,Chennai to Lessee Ayush Upadhyay for 7 years beginning from 21st September 2023
"""

completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0,
    # The maximum length of the response
    max_output_tokens=1500,
)

print(completion.result)
