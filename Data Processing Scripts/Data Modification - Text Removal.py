# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import pandas as pd
from tqdm import tqdm
import random
#%%
def random_removal_of_sentences(sample_text):
    """
    This function takes a sample from the ddxplus test set as input and returns a modified version of that input. 
    The output is modified by randomly removing sentences from the medical history section.

    Args:
        sample_text: a string of sample text

    Returns:
        modified_sample: a string with parts of medical history section removed

    """
    # split the text from where the symtoms section starts
    split_text = sample_text.split("\nSymptoms:\n")
    split_text.insert(1,"Symptoms:") # insert back the "Symptoms:" part as it get removed during spliting
    
    sents = split_text[0].split('\n')
    
    # Getting indices of sentences that start with "- "
    # In other words getting indices for sentences that are related to medical history.
    sent_indices = [index for index, sent in enumerate(sents) if sent.startswith('- ')]
    
    # randomly remove 50, 60, 70, 80, 90 or 100 percent of the sentences
    removal_percent = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    
    # Randomly select of the sentences for paraphrasing
    num_to_select = int(removal_percent * len(sent_indices))
    idx_for_sents_to_remove = random.sample(sent_indices, num_to_select)
    
    filtered_sents = []
    
    # remove selected sentences based on index
    for idx, sent in enumerate(sents):
        if idx not in idx_for_sents_to_remove:
            filtered_sents.append(sent)
        
    modified_text = '\n'.join(filtered_sents)
    split_text[0] = modified_text
    modified_sample = "\n".join(split_text)
    
    return modified_sample
#%%
def main():
    file_name = 'sampled_classification_data/test_set.csv'
    test_df = pd.read_csv(file_name)
    
    col_names = list(test_df.columns)
    new_test_df = pd.DataFrame(columns = col_names)
    
    for idx in tqdm(range(len(test_df))):
        text = test_df['text'][idx]
        new_text = random_removal_of_sentences(text)
        
        temp_df = pd.DataFrame([{'text': new_text, 'related_labels': test_df['related_labels'][idx], 
                                 'all_labels': test_df['all_labels'][idx], 'pathology': test_df['pathology'][idx]}])
        
        new_test_df = pd.concat([new_test_df, temp_df] , axis=0, ignore_index=True)
        
    
    new_test_df.to_csv("test_set_with_text_removal.csv", index=False)

if __name__ == '__main__':
    main()