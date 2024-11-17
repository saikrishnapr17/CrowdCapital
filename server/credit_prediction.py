import joblib
import numpy as np
import pandas as pd

def prediction(income, loans):
    model = joblib.load('../credit_score_model2.pkl')

    features = [
        'Delay_from_due_date', 'Num_of_Delayed_Payment', 
        'Num_Credit_Inquiries', 'Amount_invested_monthly', 
        'Total_EMI_per_month', 'Credit_Utilization_Ratio',
        'Monthly_Inhand_Salary', 'Interest_Rate', 'Num_of_Loan'
    ]

    new_data = pd.DataFrame([[
        21, 13, 5, 49.66, 45.47, 33.13, income, 14, loans
    ]], columns=features)

    # Predict using the model
    predictions = model.predict(new_data)
    return(predictions[0])
