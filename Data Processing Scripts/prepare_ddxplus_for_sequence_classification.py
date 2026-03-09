# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import pandas as pd
from preprocess_utils import generate_dataset
from sklearn.model_selection import train_test_split 
#%%

def main():
    # set this value to False if you don't want to create training set while running this script
    generate_train_set = False
    # set this value to False if you don't want to apply any modifications to the training data
    apply_modifications_on_train_set = True
    
    # set this value to False if you don't want to create validation set while running this script
    generate_valid_set = False
    # set this value to False if you don't want to create test set while running this script
    generate_test_set = True
    
    # load dataframes from disk.
    evidences_df_new = pd.read_csv('csv_files/release_evidences_new.csv')
    values_df = pd.read_csv('csv_files/value_meanings.csv')
    values_df_new = pd.read_csv('csv_files/value_meanings_new.csv')
    train_df = pd.read_csv('sampled_ddxplus_data/sampled_train_data.csv')
    #test_df = pd.read_csv('sampled_ddxplus_data/sampled_test_data.csv') 
    test_df = pd.read_csv('sampled_ddxplus_data/release_test_patients.csv')
    valid_df = pd.read_csv('sampled_ddxplus_data/sampled_validation_data.csv')    
    
    # number of classes/labels
    dataset_labels = list(train_df['PATHOLOGY'].unique())
    print("Number of unique diseases-" , len(dataset_labels))
    
    # train set generation
    if generate_train_set == True:
        if apply_modifications_on_train_set == True:
            # select 30% of training data for applying modifications
            train_set_unchanged, train_set_modifiable = train_test_split(train_df, random_state=117, test_size=0.3)
            # divide the selected 30% data equally to apply paraphrasing and introducing medical term diversity
            set_for_paraphrase, set_for_medical_term_diversity = train_test_split(train_set_modifiable, random_state=117, 
                                                                                  test_size=0.5)
           
            
            train_dataset_unchanged = generate_dataset(train_set_unchanged, dataset_labels, evidences_df_new, 
                                                       values_df, values_df_new)
            # generates an un-modified dataset. The paraphrasing will be applied later using a separate script.
            train_dataset_for_paraphrase = generate_dataset(set_for_paraphrase, dataset_labels, evidences_df_new, 
                                                       values_df, values_df_new)
            # generates a modified dataset where the medical terms are further diversified
            train_dataset_for_medical_term_diversity = generate_dataset(set_for_medical_term_diversity, dataset_labels, 
                                                                        evidences_df_new, values_df, values_df_new,
                                                                        use_alternative_med_terms = True)
            
            train_dataset_unchanged.to_csv('train_set_unchanged.csv', index=False)
            train_dataset_for_paraphrase.to_csv('train_set_for_paraphrasing.csv', index=False)
            train_dataset_for_medical_term_diversity.to_csv('train_set_with_med_term_diversity.csv', index=False)
            
        else:
            train_dataset = generate_dataset(train_df, dataset_labels, evidences_df_new, values_df, values_df_new)
            train_dataset.to_csv('train_set.csv', index=False)
    
    #validation set generation
    if generate_valid_set == True:
        # no modification is applied to the test or validation datasets
        valid_dataset = generate_dataset(valid_df, dataset_labels, evidences_df_new, values_df, values_df_new)
        valid_dataset.to_csv('validation_set.csv', index=False)
        
    #validation set generation
    if generate_test_set == True:
        # no modification is applied to the test or validation datasets
        test_dataset = generate_dataset(test_df, dataset_labels, evidences_df_new, values_df, values_df_new)
        test_dataset.to_csv('test_set.csv', index=False)
        
    
if __name__ == '__main__':
    main()
