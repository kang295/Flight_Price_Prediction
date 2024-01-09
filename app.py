from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        date_arr = request.form["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)
        Total_Stops = int(request.form["stops"])
        airline = request.form['airline']
        if (airline == 'Jet Airways'):
            Airline_JetAirways = 1
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'IndiGo'):
            Airline_JetAirways = 0
            Airline_IndiGo = 1
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'Air India'):
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'Multiple carriers'):
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'SpiceJet'):
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'Vistara'):
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 1
            Airline_GoAir = 0
            Airline_Other = 0
        elif (airline == 'GoAir'):
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 1
            Airline_Other = 0
        else:
            Airline_JetAirways = 0
            Airline_IndiGo = 0
            Airline_AirIndia = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_GoAir = 0
            Airline_Other = 1
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
        elif (Source == 'Kolkata'):
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0
        elif (Source == 'Mumbai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0
        elif (Source == 'Chennai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1
        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            Destination_Cochin = 1
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif (Source == 'Delhi'):
            Destination_Cochin = 0
            Destination_Delhi = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif (Source == 'Hyderabad'):
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0
        elif (Source == 'Kolkata'):
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1
        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        prediction = model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            Duration_hour,
            Duration_mins,
            Airline_JetAirways,
            Airline_IndiGo,
            Airline_AirIndia,
            Airline_MultipleCarriers,
            Airline_SpiceJet,
            Airline_Vistara,
            Airline_GoAir,
            Airline_Other,
            Source_Kolkata,
            Source_Mumbai,
            Source_Chennai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata
        ]])
        output_inr = round(prediction[0], 2)
        conversion_rate = 0.012
        output_usd = round(output_inr * conversion_rate, 2)
        return render_template('home.html', prediction_text="Your Flight price is {} INR or ({} USD).".format(output_inr, output_usd))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
