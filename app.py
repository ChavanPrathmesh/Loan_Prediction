
# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit_history = float(request.form['credit_history'])
        area = request.form['area']
        ApplicantIncome = float(request.form['applicantincome'])
        CoapplicantIncome = float(request.form['coapplicantincome'])
        LoanAmount = float(request.form['loanAmount'])
        Loan_Amount_Term = float(request.form['loan_amount_term'])

        # gender
        if(gender == "Male"):
            Gender = 1
        else:
            Gender = 0

        # married
        if(married == 'Yes'):
            Married = 1
        else:
            Married = 0

        # dependents
        if(dependents == '1'):
            Dependents = 1
        elif(dependents == '2'):
            Dependents = 2
        elif(dependents == "3+"):
            Dependents = 3
        else:
            Dependents = 0        

        # education
        if (education == "Graduate"):
            Education = 1
        else:
            Education = 0

        # employed
        if (employed == "Yes"):
            Self_Employed = 1
        else:
            Self_Employed = 0

        # property area
        if(area == "Urban"):
            Property_Area = 1
        elif(area == "Rural"):
            Property_Area = 2
        else:
            Property_Area = 0

        Credit_History = credit_history
        ApplicantIncomeLog = np.log(ApplicantIncome)
        CoapplicantIncomeLog = np.cbrt(CoapplicantIncome)
        Total_Income_Log = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountLog = np.log(LoanAmount)
        Loan_Amount_Term_Log = np.square(Loan_Amount_Term)

        prediction = model.predict([[Gender, Married, Dependents, Education, Self_Employed, Credit_History, Property_Area,
                                       ApplicantIncomeLog, CoapplicantIncomeLog, LoanAmountLog, Loan_Amount_Term_Log, Total_Income_Log]])

        # prediction
        if(prediction == 1):
            prediction="Yes"
        else:
            prediction="No"
        
        return render_template('prediction.html', prediction_text='Loan Status is {}'.format(prediction))

    else:
        return render_template('prediction.html')


if __name__ == "__main__":
    app.run(debug=True)
