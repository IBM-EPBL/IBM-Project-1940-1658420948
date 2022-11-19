from flask import Flask, request, render_template
import joblib
import pandas as pd

RanFor = joblib.load(open("finalized_model_ibm.pkl", 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('inputform.html')

@app.route('/', methods=["POST"])
def upload():
    if request.method == "POST":
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
        vect = {}
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

        df = pd.DataFrame.from_records(vect, index=[0])
        crop_yield = RanFor.predict(df)[0]
        if(str(crop_yield) == '1'):
            msg = "Status: Liver Disease Positive"
        else:
            msg = "Status: Liver Disease Negative"
        return render_template('inputform.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
