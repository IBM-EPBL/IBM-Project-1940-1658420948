from flask import Flask, render_template,request
import requests
import joblib
import pandas as pd

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.


app = Flask(_name_)

@app.route('/')
def home():
    return render_template('inputform.html')

@app.route('/', methods=["POST"])
def upload():
    if request.method == "POST":
        API_KEY = "frcKpzAHOm195t5SOcXp_nuH1EUqjG3q4iUpZONkxSP9"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        print(token_response.json())
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        name = request.form.get("name")
        emailid = request.form.get("emailid")
        age = int(request.form.get("age"))
        total_bilirubin = float(request.form.get("total_bilirubin"))
        direct_bilirubin = float(request.form.get("direct_bilirubin"))
        alkaline_phosphate = int(request.form.get("alkaline_phosphate"))
        alamine_aminotransferase = int(request.form.get("alamine_aminotransferase"))
        aspartate_aminotransferase = int(request.form.get("aspartate_aminotransferase"))
        total_proteins = float(request.form.get("total_proteins"))
        albumin = float(request.form.get("albumin"))
        albumin_and_globulin_ratio = float(request.form.get("albumin_and_globulin_ratio"))

        X = ['Age', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
             'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 'Albumin_and_Globulin_Ratio']

        index_dict = dict(zip(X, range(len(X))))
        vect={}
        vect1 = [int(total_bilirubin),int(direct_bilirubin),int(alkaline_phosphate),int(alamine_aminotransferase),int(aspartate_aminotransferase),int(total_proteins),int(albumin),int(albumin_and_globulin_ratio)]
        for key, val in index_dict.items():
            vect[key] = 0
        vect['Age'] = age
        vect['Total_Bilirubin'] = total_bilirubin
        vect['Direct_Bilirubin'] = direct_bilirubin
        vect['Alkaline_Phosphotase'] = alkaline_phosphate
        vect['Alamine_Aminotransferase'] = alamine_aminotransferase
        vect['Aspartate_Aminotransferase'] = aspartate_aminotransferase
        vect['Total_Protiens'] = total_proteins
        vect['Albumin'] = albumin
        vect['Albumin_and_Globulin_Ratio'] = albumin_and_globulin_ratio
        
        payload_scoring = {"input_data": [{"fields": [X], "values": [vect1]}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/21e926ef-d143-4738-978f-25d6f5bc8021/predictions?version=2022-11-18', json=payload_scoring,
         headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        print(predictions['predictions'][0]['values'][0][0])
        return render_template('inputform.html', msg=msg)



if _name_ == '_main_':
    app.run()