import pandas as pd
import openai
import csv



openai.api_key="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"

# prompt = "The following is an abstract from a scientific paper. \n\nThe user want to extract the keywords related to autism. Can you generate a list of keywords\n\n"

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Specify the ChatGPT model variant
        prompt=prompt,
        temperature=0,  # Adjust the creativity of the response
    )
    
    # Retrieve and return the generated response
    message = response.choices[0].text.strip()
    return message

with open('abstracts.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        prompt = f"""The following is an abstract from a scientific paper. \n\nThe user want to extract the keywords related to autism. Can you generate a list of keywords\n\n```{row[1]}```"""
        keywords=chat_with_gpt(prompt)
        df2 = pd.DataFrame([[row[1],row[2],keywords,row[4]]], columns=['Title','Abstract','Keywords','Link'])