# Automatic-Differential-Diagnosis-using-Transformers
This repository contains the official source code of the findings presented in the paper [Automatic Differential Diagnosis using Transformer-Based Multi-Label Sequence Classification](https://doi.org/10.48550/arXiv.2408.15827).

## Implementation Overview
- We used the english version of the DDXPlus Dataset, which can be downloaded from [here](https://figshare.com/articles/dataset/DDXPlus_Dataset_English_/22687585). Once downloaded, the dataset should contain a total of five files:
```
├── DDXPlus\
    ├── release_conditions.json # a JSON file containing descriptions of the 49 medical condition
    ├── release_evidences.json # a JSON file containing evidence description
    ├── release_test_patients # a CSV file containing test set patient samples.
    ├── release_train_patients # a CSV file containing train set patient samples.
    ├── release_validate_patients # a CSV file containing train set patient samples.
```
**Note:** The '.csv' extension was missing on the train, test, and validation files when we downloaded the dataset. However, the contents were in CSV format and it could easily be loaded with Pandas. This may have been fixed by the authors in future versions.
- For our convenience, we converted the JSON files present in the dataset into CSV files. We provide a simple notebook for doing that using Pandas. However, this can easily be done using other methods. Our notebook can be found in the 'Data Processing Scripts' folder.
- The 'Data Processing Scripts' folder contains all the codes used for processing the DDXPlus dataset, including generation of patient reports, data modification modules, and generation of behavioral test data. The Folder contains the following files:
```
├── Data Processing Scripts\                   
    ├── Data Modification - Paraphrasing.py  # code for implementing the sequence paraphrasing module using the OpenAI API
    ├── Data Modification - Text Removal.py   # behavioral test: for generating a modified version of the test set used for the medical history exclusion test
    ├── Data Modification - Typo Generation.py  # behavioral test: for generating a modified version of the test set used for the typo insertion test
    ├── prepare_ddxplus_for_sequence_classification.py   # code finalizing the sequence classification dataset, which can then be used for Multi-label classification
    ├── preprocess_utils.py   # contains our main algorithm for converting the DDXPlus patient samples into patient reports
    ├── sample_data.py   # code for collecting a balanced set of train, test, and validation patient samples from the DDXPlus dataset
    ├── utils_for_typo.py  # contians functions for inserting different forms of typos into a given string. Used in 'Data Modification - Typo Generation.py'
    └── JSON to CSV.ipynb # for converting some of the JSON files from the DDXPlus dataset into CSV files.
```

- Since we had to use a Google Colab environment to perform our GPU-related (training and testing) experiments, the training and testing codes are in a notebook format. These codes are present in the root directory. 

```       
├── test_notebook.ipynb  # testing pipeline for all test cases, including behavioral tests.
└── train_notebook.ipynb  # multi-label classification training pipeline
```

## References
Please consider citing our paper if you find our work useful or use our source code in your own research.
 ```
@article{sadi2024automatic,
  title={Automatic Differential Diagnosis using Transformer-Based Multi-Label Sequence Classification},
  author={Sadi, Abu Adnan and Khan, Mohammad Ashrafuzzaman and Saber, Lubaba Binte},
  journal={arXiv preprint arXiv:2408.15827},
  year={2024}
}
 ```
