# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import pandas as pd
#%%
def get_balanced_sample_data(df, samples_per_category, seed):
    """
    A function that returns a balanced dataset which contains the same number of samples per ground-truth pathology (disease)
    category. If there aren't sufficient amount of samples present in a particular catergory, then the function return all the
    samples that are present for that category.
    Args:
        df: a dataframe containing training, test or validation samples
        samples_per_category: an integer for defining the number of samples that should be selected for each class/label
        seed: am integer seed value for sampling

    Returns:
        result_df: a dataframe containing the newly sampled data.
    """
    all_col_names = list(df.columns)
    target_col_name = 'PATHOLOGY'
    result_df = pd.DataFrame(columns = all_col_names)

    # collecting samples for each unique value in the target column
    for col_value in list(df[target_col_name].unique()):
        # selecting rows based on the unique column value
        filtered_df = df[df[target_col_name] == col_value]
        
        # check if there are sufficient samples available for filtering
        if len(filtered_df)> samples_per_category:
            temp_df = filtered_df.sample(samples_per_category, random_state=seed, axis=0)
        else:
            temp_df = filtered_df
        
        # concatenating sampled rows in new dataframe
        result_df = pd.concat([result_df,temp_df], axis=0, ignore_index = True)

    return result_df

#%%
def main():
    # load data
    train_df = pd.read_csv('csv_files/release_train_patients.csv')
    test_df = pd.read_csv('csv_files/release_test_patients.csv')
    valid_df = pd.read_csv('csv_files/release_validate_patients.csv')
    
    # number of classes/labels
    dataset_labels = list(train_df['PATHOLOGY'].unique())
    print("Number of unique diseases-" , len(dataset_labels))
    
    seed = 117
    train_samples_per_category = 1000
    test_samples_per_category = 100
    
    train_df_sampled = get_balanced_sample_data(train_df, train_samples_per_category, seed)
    test_df_sampled = get_balanced_sample_data(test_df, test_samples_per_category, seed)
    valid_df_sampled = get_balanced_sample_data(valid_df, test_samples_per_category, seed)
    
    print("Number of samples in train dataset: ", len(train_df_sampled))
    print("Number of samples in test dataset: ", len(test_df_sampled))
    print("Number of samples in validation dataset: ", len(valid_df_sampled))
    
    train_df_sampled.to_csv('sampled_train_data.csv', index=False)
    test_df_sampled.to_csv('sampled_test_data.csv', index=False)
    valid_df_sampled.to_csv('sampled_validation_data.csv', index=False)

if __name__ == '__main__':
    main()
