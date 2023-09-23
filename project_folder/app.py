# from flask import Flask, request, jsonify
# import pandas as pd
# from datetime import datetime, timedelta
#
# app = Flask(__name__)
#
# # Sample DataFrame with change request data (you would replace this with your actual data)
# data = {
#     'CR_ID': range(1, 13),
#     'Type': ['Normal', 'Urgent', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Normal'],
#     'Change_Opened_By': ['User1', 'User2', 'User1', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10', 'User11'],
#     'Short_Desc': [
#         'This is a normal change request with more than 50 characters.',
#         'Urgent CR',
#         'Normal CR',
#         'Another normal CR with a long description that contains all questions.',
#         'Normal CR with missing data.',
#         'Normal CR with CAB calendar and planned start time.',
#         'Normal CR without CAB calendar and planned start time in the future.',
#         'Normal CR with Risk: High, Impact: Critical, CAB calendar, and successful testing.',
#         'Normal CR with Risk: High, Impact: High, CAB calendar, and successful testing.',
#         'Normal CR with Risk: Low, Impact: Low, CAB calendar, and successful testing.',
#         'Normal CR with Risk: High, Impact: Critical, CAB calendar, and Pre-Imp Testing: None.',
#         'Normal CR with Risk: High, Impact: High, CAB calendar, and Pre-Imp Testing: N/A.'
#     ],
#     # ... (other columns)
# }
#
# # Load the data into a DataFrame
# df = pd.DataFrame(data)
#
# # Function to apply the rule-based model and determine CR outcome
# def determine_cr_outcome(row):
#     if(
#         row['Type'] == 'Normal' and
#         row['Change_Opened_By'] !=row['Short_Desc']
#     ):
#         return 'Accepted'
#     else:
#         return 'Rejacted'
#     # Rules...
#     # (Same rules as in the previous code example)
#     # ...
#
# @app.route('/predict_data', methods=['POST'])
# def predict_cr_outcome():
#     try:
#         # Receive JSON data for a new cha
#         # nge request
#         #new_data = request.get_json()
#         new_data = {
#             'Type': 'Normal',
#             'Change_Opened_By': 'abc',
#             'Short_Desc': 'This is first change request'
#         }
#
#         # Create a DataFrame from the received JSON data
#         new_df = pd.DataFrame([new_data])
#
#         # Apply the rule-based model to determine CR outcome
#         new_df['CR_Outcome'] = new_df.apply(determine_cr_outcome, axis=1)
#
#         # Extract the predicted outcome for the new request
#         predicted_outcome = new_df['CR_Outcome'].iloc[0]
#
#         # Return the prediction as a JSON response
#         response = {'predicted_outcome': predicted_outcome}
#         return jsonify(response), 200
#
#     except Exception as e:
#         error_message = str(e)
#         return jsonify({'error': error_message}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#

#
# from flask import Flask, render_template, request
# import pandas as pd
# import numpy as np
#
# app = Flask(__name__)
#
# # Sample CR data (you can replace this with your actual data)
# data = {
#     'CR_ID': range(1, 101),
#     'Status': np.random.choice(['Open', 'In Progress', 'Closed'], size=100),
#     'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100),
#     'Created_Date': pd.date_range(start='2023-01-01', periods=100),
# }
#
# # Create a DataFrame
# df = pd.DataFrame(data)
#
# # Function to apply the rule-based model
# def rule_based_model(row):
#     if row['Priority'] == 'High':
#         return 'In Progress'
#     elif row['Priority'] == 'Medium' and row['Created_Date'].weekday() >= 3:
#         return 'In Progress'
#     else:
#         return 'Open'
#
# # Apply the rule-based model to predict CR status
# df['Predicted_Status'] = df.apply(rule_based_model, axis=1)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # priority = request.form['priority']
#         priority ='High'
#         # created_date = pd.to_datetime(request.form['created_date'])
#         created_date = '2023-01-01'
#         # Apply the rule-based model to predict the status for the user's input
#         predicted_status = rule_based_model({'Priority': priority, 'Created_Date': created_date})
#         return render_template('index.html', prediction=predicted_status)
#     return render_template('index.html', prediction=None)
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Sample CR data (you can replace this with your actual data)
data = {
    'CR_ID': range(1, 101),
    'Status': np.random.choice(['Open', 'In Progress', 'Closed'], size=100),
    'Priority': np.random.choice(['High', 'Medium', 'Low'], size=100),
    'Created_Date': pd.date_range(start='2023-01-01', periods=100),
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to apply the rule-based model
def rule_based_model(row):
    if row['Priority'] == 'High':
        return 'In Progress'
    elif row['Priority'] == 'Medium' and row['Created_Date'].weekday() >= 3:
        return 'In Progress'
    else:
        return 'Open'

# Apply the rule-based model to predict CR status
df['Predicted_Status'] = df.apply(rule_based_model, axis=1)

@app.route('/predict', methods=['POST'])
def predict_status():
    try:
        data = request.json  # Get JSON data from the request
        priority = data['priority']
        created_date = pd.to_datetime(data['created_date'])
        # Apply the rule-based model to predict the status based on input data
        predicted_status = rule_based_model({'Priority': priority, 'Created_Date': created_date})
        response = {'predicted_status': predicted_status}
        return jsonify(response)  # Respond with JSON data
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
