#!/bin/bash

# Exit immediately if any command fails
set -e

echo "======================================================"
echo " Starting the DDXPlus Data Processing Pipeline"
echo "======================================================"

# Navigate to the scripts directory
cd "Data Processing Scripts"

# Step 0: JSON to CSV conversion
# Note: Since this is a Jupyter Notebook, it's commented out by default. 
# If you have jupyter installed, you can uncomment the line below to run it programmatically.
# echo "Step 0: Converting JSON to CSV..."
# jupyter nbconvert --to notebook --execute "JSON to CSV.ipynb"

echo "Step 1: Sampling balanced data..."
python sample_data.py

echo "Step 2: Preparing dataset for sequence classification..."
# This script internally calls functions from preprocess_utils.py
python prepare_ddxplus_for_sequence_classification.py

echo "Step 3: Generating paraphrased training data..."
# WARNING: This requires a valid OPENAI_API_KEY in your .env file
python "Data Modification - Paraphrasing.py"

echo "Step 4: Generating behavioral test data (Typo Generation)..."
python "Data Modification - Typo Generation.py"

echo "Step 5: Generating behavioral test data (Text Removal)..."
python "Data Modification - Text Removal.py"

echo "======================================================"
echo " Pipeline execution completed successfully!"
echo "======================================================"