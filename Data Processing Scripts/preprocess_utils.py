# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""
import pandas as pd
import ast
from tqdm import tqdm
import random
#%%
# definitions for all the necessary functions

def get_special_case_responses(ev_value, ev_info):
    """
    This function returns the associated text for special cases where the response to a 
    multi-choice evidence is only in positive, negative or null terms.
    
    Args:
        ev_value: a string containing the multi choice answer value for an specific evidence
        ev_info: contains row information regarding an specific evidence from the evidences dataframe
    Returns:
        response: a string containing textual response for the evidence
    """
    # if answer value is NA or 'nowhere', then select the negative response text
    if ev_value == "V_123" or ev_value == "V_11":
        response = f"- {ev_info['answer_neg'].values[0]}"
        
    # if answer value is 'no', then also select the negative response text   
    elif ev_value == "V_10":
        response = f"- {ev_info['answer_neg'].values[0]}"
    
    # if answer value is 'yes', then select the positive response text  
    elif ev_value == "V_12":
        response = f"- {ev_info['answer_pos'].values[0]}"
    
    return response

def get_patient_report(patient, evidences_df, values_df, values_df_new, use_alternative_med_terms = False):
    """
    This function generates a patient report containing the medical history and symoptoms described by the patient. The
    function takes a row from one of the train, test or validation dataframes, and converts it into textual information
    that is suitable for training a sequencec classification model.
    
    Args:
        patient: a dictory containing all the information regarding a patient.
        evidences_df: a dataframe containing information regarding all of the evidences present in the DDXPlus dataset.
        values_df: a dataframe containing information regarding all the unique values that a multi-choice or catergorical
                   evidence can have.
        value_df_new: a dataframe containing additional information for each unique value(medical terms) in values_df. 
                      It contains an additional column which contains lists of synonyms and related terminology for each 
                      medical term.
        use_alternative_med_terms: a boolean variable. Setting it to 'True' will apply modifications to the medical terms
                                   by replacing them with synonyms or other related terms. The variable defaults to False.
    Returns:
        prompt: a string which containing the all the necessary patient information including age, sex, medical history
                and symptoms.
    """
    
    if patient['SEX'] == 'M':
        prompt = f"""The following is a list of medical history and symptoms described by a patient.\nSex: Male, Age: {patient['AGE']}\n"""   
    else:
        prompt = f"""The following is a list of medical history and symptoms described by a patient.\nSex: Female, Age: {patient['AGE']}\n"""

    list_symptoms = [] # list of comments related to symptoms
    list_medhist = [] # list of comments related to medical history

    # ast.literal_eval() is used to convert the string representation of the list into an actual python list
    for evidence in ast.literal_eval(patient['EVIDENCES']):

        # seperating the evidence name and value
        if "_@_" in evidence:
            # split the string into parts
            parts = evidence.split("_@_")
            ev_name = parts[0]
            ev_value = parts[1]

            # getting the specific evidence information from the evidences table
            ev_info = evidences_df[evidences_df['name'] == ev_name]

            # seperating the medical history information
            if ev_info['is_antecedent'].values[0] == True:
                # special cases where the response is only in positive, negative or null terms
                if ev_value in ['V_123', 'V_11', 'V_10', 'V_12']:
                    temp_ans = get_special_case_responses(ev_value, ev_info)
                    list_medhist.append(temp_ans)
                else:
                    # getting the answer from the values dataframe
                    if use_alternative_med_terms == False:
                        ans = values_df[values_df['index'] == ev_value]['en'].values[0] if ev_value.startswith('V') else f"{ev_value}"
                    else:
                        # the 'ans' variable is a list of alternative medical terms if ev_value starts with 'V'
                        ans = ast.literal_eval(values_df_new[values_df_new['index'] == ev_value]['en_alternative'].values[0]) if ev_value.startswith('V') else f"{ev_value}"
                        ans = random.choice(ans) if isinstance(ans, list) else ans
                        
                    temp_ans = f"- {ev_info['answer_pos'].values[0]} {ans}."
                    list_medhist.append(temp_ans)

            # seperating the symptoms information
            else:
                # special cases where the response is only in positive, negative or null terms
                if ev_value in ['V_123', 'V_11', 'V_10', 'V_12']:
                    temp_ans = get_special_case_responses(ev_value, ev_info)
                    list_symptoms.append(temp_ans)
                else: 
                    # getting the answer from the values dataframe
                    if use_alternative_med_terms == False:
                        ans = values_df[values_df['index'] == ev_value]['en'].values[0] if ev_value.startswith('V') else f"{ev_value}"
                    else:
                        # the 'ans' variable is a list of alternative medical terms if ev_value starts with 'V'
                        ans = ast.literal_eval(values_df_new[values_df_new['index'] == ev_value]['en_alternative'].values[0]) if ev_value.startswith('V') else f"{ev_value}"
                        ans = random.choice(ans) if isinstance(ans, list) else ans
                        
                    temp_ans = f"- {ev_info['answer_pos'].values[0]} {ans}."
                    list_symptoms.append(temp_ans)

        else:
            ev_name = evidence
            ev_info = evidences_df[evidences_df['name'] == ev_name]

            if ev_info['is_antecedent'].values[0] == True:
                temp_ans = f"- {ev_info['answer_pos'].values[0]}"
                list_medhist.append(temp_ans)
            else:
                temp_ans = f"- {ev_info['answer_pos'].values[0]}"
                list_symptoms.append(temp_ans)


    #inserting medical history into the prompts
    prompt += f"Medical History:\n"
    for i, answer in enumerate(list_medhist):
        prompt += f"{answer}\n"

    #inserting symptoms into the prompts
    prompt += f"Symptoms:\n"
    for i, answer in enumerate(list_symptoms):
        prompt += f"{answer}\n"
        
    return prompt


def generate_dataset(df, dataset_labels, evidences_df, values_df, values_df_new, use_alternative_med_terms = False):
    """
    This function takes the data from the DDXPlus train, test and validation sets and prepares them for the multi-label 
    classification task.
    Args:
        df: a dataframe containing raw train, test or validation data.
        dataset_labels: a list of all the dataset labels.
        evidences_df: a dataframe containing information regarding all of the evidences present in the DDXPlus dataset.
        values_df: a dataframe containing information regarding all the unique values that a multi-choice or catergorical
                   evidence can have.
        value_df_new: a dataframe containing additional information for each unique value(medical terms) in values_df. 
                      It contains an additional column which contains lists of synonyms and related terminology for each 
                      medical term.
        use_alternative_med_terms: a boolean variable. Setting it to 'True' will apply modifications to the medical terms
                                   by replacing them with synonyms or other related terms. The variable defaults to False.

    Returns:
        dataset_df: a dataframe containing train, test or validation data that is suitable for multi-label 
                    sequence classification
    """
    col_names = ['text', 'related_labels', 'all_labels', 'pathology']
    dataset_df = pd.DataFrame(columns = col_names)
    
    for i in tqdm(range(len(df))):
        patient = df.iloc[i].to_dict()
        
        # generating a patient report prompt using the patient data
        report = get_patient_report(patient, evidences_df, values_df, values_df_new, use_alternative_med_terms)
        
        # collecting diagnosis labels
        diag_info = ast.literal_eval(patient['DIFFERENTIAL_DIAGNOSIS'])
        labels_list = []
        for diag in diag_info:
            labels_list.append(diag[0])
        
        if i == 0:
            temp_df = pd.DataFrame([{'text': report, 'related_labels': labels_list, 
                                     'all_labels':dataset_labels, 'pathology': patient['PATHOLOGY']}])
        else:
            temp_df = pd.DataFrame([{'text': report, 'related_labels': labels_list, 'pathology': patient['PATHOLOGY']}])
        
        dataset_df = pd.concat([dataset_df, temp_df] , axis=0, ignore_index=True)
    
    return dataset_df