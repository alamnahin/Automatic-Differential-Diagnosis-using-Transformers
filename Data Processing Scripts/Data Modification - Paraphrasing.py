# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import pandas as pd
import os
from tqdm import tqdm
import random

from openai import OpenAI
from dotenv import load_dotenv
#%%
def process_response(res):
    """
    This function takes the response from the GPT api as input, which contains a certain number of paraphrases.
    It then converts it into a python list, where each element is a candidate paraphrase sentence.
    
    args:
        res: response string from the api
    return:
        res_list: response converted to a list
    """
    # Split the string to get a list with individual elements
    res_list = res[2:-2].split("', '")
    
    return res_list

def paraphrase(sentence, client):
    response = client.chat.completions.create(
                  model="gpt-3.5-turbo-0125",
                  messages=[
                    {
                      "role": "system",
                      "content": "You will be provided with a sentence. Your job is to return three different paraphrases for the given sentence, and the paraphrased sentences should retain the meaning of the original sentence. You should also return the paraphrased sentences in a Python list format."
                    },
                    {
                      "role": "user",
                      "content": "I have some family members who have been diagnosed with anemia."
                    },
                    {
                      "role": "assistant",
                      "content": "['Some of my relatives have been found to have anemia.', 'Anemia has been detected in certain individuals within my family circle.', 'There are family members of mine who have received a diagnosis of anemia.']"
                    },
                    {
                      "role": "user",
                      "content": sentence
                    },
                  ],
                  temperature=0.8,
                  max_tokens=512,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
             )
    para_sentence_list = process_response(response.choices[0].message.content)
    return para_sentence_list

def get_paraphrased_sample(sample_text, client):
    sents = sample_text.split('\n')
    
    # Getting indices of sentences that start with "- "
    # In other words getting indices for sentences that are related to medical history and symptoms.
    sent_indices = [index for index, sent in enumerate(sents) if sent.startswith('- ')]
    
    # Randomly select 40% of the sentences for paraphrasing
    num_to_select = int(0.4 * len(sent_indices))
    idx_for_sents_to_paraphrase = random.sample(sent_indices, num_to_select)
    
    for idx in idx_for_sents_to_paraphrase:
        text = sents[idx]
        # remove the hyphen at start
        text = text.replace("- ","")
        
        # getting a list of 5 possible paraphrases
        para_sent_list = paraphrase(text, client)
        # selecting on the possible paraphrases from the list
        selected_para_sent = random.choice(para_sent_list)
        # add the hyphen back at the start
        selected_para_sent = "- " + selected_para_sent
        
        sents[idx] = selected_para_sent
    
    modified_sample = '\n'.join(sents)
    return modified_sample
#%%
def main():
    # loading variables from .env file
    load_dotenv() 
    api_key = os.getenv("OPENAI_API_KEY")
    
    client = OpenAI(api_key=api_key)
    
    file_name = 'sampled_classification_data/train_set_for_paraphrasing.csv'
    df = pd.read_csv(file_name)
    
    col_names = list(df.columns)
    new_df = pd.DataFrame(columns = col_names)
    
    for idx in tqdm(range(len(df))):
        text = df['text'][idx]
        new_text = get_paraphrased_sample(text, client)
            
        temp_df = pd.DataFrame([{'text': new_text, 'related_labels': df['related_labels'][idx], 
                                     'all_labels': df['all_labels'][idx], 'pathology': df['pathology'][idx]}])
            
        new_df = pd.concat([new_df, temp_df] , axis=0, ignore_index=True)
        
    new_df.to_csv("train_set_paraphrased.csv", index=False)
    

if __name__ == '__main__':
    main()