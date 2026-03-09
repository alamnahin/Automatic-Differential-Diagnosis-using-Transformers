# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import pandas as pd
import random
import math
from tqdm import tqdm
from nltk.tokenize import word_tokenize
import nltk
from string import punctuation
from string import digits
from utils_for_typo import replace_with_adjacent_char, add_extra_adjacent_char, swap_consecutive_chars, skip_char, repeat_char

nltk.download('punkt')
nltk.download('wordnet')
#%%
def get_typo_introduced_sample(sample_text):
    """
    This function takes a sample from the ddxplus test set as input and returns a modified version of that input. 
    The output is modified by randomly introducing typos to the input text.

    Args:
        sample_text: a string of sample text

    Returns:
        modified_sample: a string containing typo introduced text

    """
    
    punctuation_list = list(punctuation)
    digits_list = list(digits)
    #custom terms
    custom_terms = ['0-10', '10', '18.5','r', 'l', '\'s', '1cm']
    
    # split text into sentences
    sents = sample_text.split('\n')
    # Getting indices of sentences that start with "- "
    # In other words getting indices for sentences that are related to medical history and symptoms.
    sent_indices = [index for index, sent in enumerate(sents) if sent.startswith('- ')]
    
    # Randomly select 50% of the sentences for adding typos
    num_to_select = int(0.5 * len(sent_indices))
    idx_for_sents_to_add_typos = random.sample(sent_indices, num_to_select)
    
    for idx in idx_for_sents_to_add_typos:
        text = sents[idx]
        
        words = word_tokenize(text)
        
        filtered_words = {} 
        # remove punctuations, digits, custom stop terms and terms with only a single char
        for index, word in enumerate(words):
            if word.lower() in custom_terms:
                continue
            elif set(word).intersection(set(punctuation_list)) or set(word).intersection(set(digits_list)):
                continue
            elif len(word)<2:
                continue
            else:
                filtered_words[index] = word
        
        # Randomly select 15% of the words to add typos
        num_to_select = math.ceil(0.15 * len(filtered_words)) if len(filtered_words) > 1 else len(filtered_words)
        words_to_change = random.sample(list(filtered_words.keys()), num_to_select)
        
        # list of functions for introducing typos
        typo_types = [replace_with_adjacent_char, add_extra_adjacent_char, swap_consecutive_chars, skip_char, repeat_char]
        
        for key in words_to_change:
            word = filtered_words[key]
            typo_type = random.choice(typo_types)
            
            typo_word = typo_type(word)
            words[key] = typo_word
            
        new_sent = ' '.join(words[:len(words)-1])
        new_sent += words[len(words)-1] # separately adding the full stop character at the end
        
        sents[idx] = new_sent
    
    modified_sample = '\n'.join(sents)
    return modified_sample
#%%
def main():
    file_name = 'sampled_classification_data/test_set.csv'
    test_df = pd.read_csv(file_name)
    
    col_names = list(test_df.columns)
    new_test_df = pd.DataFrame(columns = col_names)
    
    
    for idx in tqdm(range(len(test_df))):
        text = test_df['text'][idx]
        new_text = get_typo_introduced_sample(text)
        
        temp_df = pd.DataFrame([{'text': new_text, 'related_labels': test_df['related_labels'][idx], 
                                 'all_labels': test_df['all_labels'][idx], 'pathology': test_df['pathology'][idx]}])
        
        new_test_df = pd.concat([new_test_df, temp_df] , axis=0, ignore_index=True)
        
    
    new_test_df.to_csv("test_set_with_typos.csv", index=False)


if __name__ == '__main__':
    main()
    