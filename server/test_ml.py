import pandas as pd
import numpy as np

# Load the dataset
file_path = "../train.csv"
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
print("Initial dataset:")
print(data.head())

def calculate_adjusted_credit_score(row):
    # Assign weights to each factor
    weights = {
        'delay_days': -0.2,
        'delayed_payments': -0.3,
        'credit_inquiries': -0.2,
        'invested_monthly': 0.3,
        'total_emi': -0.1
    }
    
    # Normalize values
    delay_days_normalized = min(max(row['Delay_from_due_date'] / 30, 0), 1)
    delayed_payments_normalized = min(max(row['Num_of_Delayed_Payment'] / 10, 0), 1)
    credit_inquiries_normalized = min(max(row['Num_Credit_Inquiries'] / 10, 0), 1)
    invested_monthly_normalized = min(max(row['Amount_invested_monthly'] / 1000, 0), 1)
    total_emi_normalized = min(max(row['Total_EMI_per_month'] / 1000, 0), 1)
    
    # Calculate the weighted score
    score = (
        weights['delay_days'] * delay_days_normalized +
        weights['delayed_payments'] * delayed_payments_normalized +
        weights['credit_inquiries'] * credit_inquiries_normalized +
        weights['invested_monthly'] * invested_monthly_normalized +
        weights['total_emi'] * total_emi_normalized
    )
    
    # Normalize score to the range 0-1
    score_normalized = min(max((score + 1) / 2, 0), 1)
    
    # Map classification to score range
    credit_score_bounds = {
        'Poor': (580, 624),
        'Standard': (625, 709),
        'Good': (710, 769),
        'Very Good': (770, 799),
        'Exceptional': (800, 850)  # Assuming 850 as a hypothetical upper bound
    }
    
    # Get the range for the classification
    classification = row['Credit_Score']
    lower_bound, upper_bound = credit_score_bounds.get(classification, (580, 850))
    
    # Scale the normalized score to the classification range
    score_adjusted = lower_bound + score_normalized * (upper_bound - lower_bound)
    
    # Ensure the score stays within the classification bounds
    return round(min(max(score_adjusted, lower_bound), upper_bound))


# Apply the function to calculate numeric credit scores for the dataset
data['Calculated_Credit_Score'] = data.apply(calculate_adjusted_credit_score, axis=1)

# Display the updated dataset with the new calculated numeric credit score
print("\nDataset with calculated numeric credit scores:")
print(data[['Delay_from_due_date', 'Num_of_Delayed_Payment', 'Num_Credit_Inquiries', 
           'Amount_invested_monthly', 'Total_EMI_per_month', 'Calculated_Credit_Score']].head())

# Save the updated dataset to a new CSV file
updated_file_path = '../train_credit.csv'
data.to_csv(updated_file_path, index=False)

print(f"\nUpdated dataset saved to: {updated_file_path}")
