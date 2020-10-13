from flask import Flask ,render_template, redirect, url_for, session, request, logging
import requests
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
@app.route('/', methods=['GET','POST']) #landing page
def home():
    if request.method == "POST":
        age = int(request.form['age'])
        gender = request.form['gender']
        if gender.lower() == "male":
            gender = 0
        else:
            gender = 1
        height = float(request.form['height'])
        height = height/100.0
        weight = float(request.form['weight'])
        smoker = request.form['smoker']
        if smoker.lower() == "smoker":
            smoker = 1
        else:
            smoker = 0
        
        import pickle
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        pfr = loaded_model.predict([[age,gender,height,weight,smoker]])
        pfr = pfr[0]
        pfr = "%0.2f" % pfr

        if gender == 0:
            pefr=41.05-(3.5*age)+(333.7*height) #males
        else:
            pefr=-213.8-(1.3*age)+(430.3*height) #females

        pefr = "%0.2f" % pefr
        difference = abs(float(pfr)-float(pefr))
        difference = "%0.2f" % difference
        return render_template("result.html",pfr=pfr,calcpef=pefr,diff = difference)
    return render_template("index.html")

if __name__=='__main__':

	app.run(threaded=True,host="0.0.0.0",port=80)