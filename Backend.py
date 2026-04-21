from flask import Flask, request, jsonify
from flask_cors import CORS
from model import FoodCostPredictor

app = Flask(__name__)
CORS(app)

predictor = FoodCostPredictor("foodprices_output.csv")


#Get a prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    year       = int(data['year'])                          # required
    country    = data.get('country', None)                  # optional
    continent  = data.get('continent', None)                # optional
    cpi_change = data.get('cpi_change', None)               # optional
    if cpi_change is not None:
        cpi_change = float(cpi_change)

    try:
        result = predictor.predict(year, country, continent, cpi_change)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

#Get the list of valid countries
@app.route('/countries', methods=['GET'])
def countries():
    return jsonify(predictor.list_countries())


#Get the list of valid continents
@app.route('/continents', methods=['GET'])
def continents():
    return jsonify(predictor.list_continents())


#Get historical data
@app.route('/historical', methods=['GET'])
def historical():
    country   = request.args.get('country', None)
    continent = request.args.get('continent', None)

    df = predictor.get_historical(country, continent)
    return jsonify(df.to_dict(orient='records'))   # converts the DataFrame to a list of dicts


#Start the server
if __name__ == '__main__':
    app.run(debug=True)