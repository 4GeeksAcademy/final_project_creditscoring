# final_project_creditscoring

# General Objective
Develop a credit risk model to estimate the probability of default and rank customers according to their risk level.

## Specific Objectives
- Reduce financial losses from unpaid credits.
- Improve decision-making in credit approval.
- Classify customers according to their risk level.
- Automate and standardize the credit evaluation process.

The data used in this project comes from the Lending Club Loan Data, a public dataset of loans issued by the peer-to-peer lending platform Lending Club in the United States. This dataset includes applicant information, loan characteristics, and final loan status, allowing for the analysis and prediction of default risk.

# Input Variables
## A) Loan Characteristics
- loan_amnt → requested amount
- term → loan duration (36/60 months)
- int_rate → interest rate
- installment → monthly payment amount
- purpose → reason for the loan (education, car, housing, etc.)
- grade / sub_grade → internal customer rating

## B) Applicant’s Financial Characteristics
- annual_inc → annual income
- dti → debt-to-income ratio
- revol_bal → current revolving debt
- revol_util → credit line utilization percentage
- total_acc → total number of credit accounts
- open_acc → open accounts
- pub_rec → negative public records (e.g., bankruptcies)
- delinq_2yrs → number of delinquencies in the last 2 years

## C) Credit History
- earliest_cr_line → date the first credit line was opened
- inq_last_6mths → recent credit inquiries
- mths (mths_since_last_delinq) → months since last delinquency

# Output Variable (Target)
Target variable (y): loan_status reclassified as binary.

The model learns from historical data to predict the probability of default for a new applicant. Additionally, macroeconomic variables and their potential impact on payment default will also be taken into account.

# Key Questions the Data Analysis Should Answer
- Which customer characteristics are most strongly associated with default?
- What is the probability that a customer will not pay their credit?
- Which customers represent the highest credit risk?
- Where should the credit approval threshold be set?
- How does the loan amount impact the probability of default?
