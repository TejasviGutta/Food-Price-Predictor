from flask import Flask, request, jsonify
from flask_cors import CORS
from model import FoodCostPredictor

app = Flask(__name__)
CORS(app)

print("Loading model...")
predictor = FoodCostPredictor("foodprices_output.csv")
print(f"Model ready. {len(predictor.list_countries())} countries loaded.")


# Validate inputs before calling predict
def validate_inputs(year, country, continent):
    errors = []

    if year < 1000:
        errors.append(f"Year {year} is out of range.")

    if country and country not in predictor.list_countries():
        errors.append(f"Country '{country}' not found. Use /countries to see valid options.")

    if continent and not country and continent not in predictor.list_continents():
        errors.append(f"Continent '{continent}' not found. Use /continents to see valid options.")

    return errors


# Getting the Prediction from the model and sending it back to the Frontend
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Reading the inputs from Frontend
    year      = int(data['year'])
    country   = data.get('country') or None 
    continent = data.get('continent') or None

    print(f"\n[REQUEST] /predict — year={year}, country={country}, continent={continent}")

    errors = validate_inputs(year, country, continent)
    if errors:
        print(f"[INVALID] {errors}")
        return jsonify({'error': errors}), 400

    try:
        result = predictor.predict(year, country, continent)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': str(e)}), 400

    Costs = [
        f"Healthy Diet: ${result['annual_cost_healthy_diet']:,.2f}/year",
        f"Fruits & Veg: ${result['annual_cost_fruits_and_veg']:,.2f}/year",
    ]
    
    #creating the response to send back to the frontend
    response = {
        "year":       result["year"],
        "country":    country or continent or "Global",
        "continent":  continent,
        "cpi_change": result["cpi_change_used"],
        "annual_cost_healthy_diet": result["annual_cost_healthy_diet"],
        "annual_cost_fruits_and_veg": result["annual_cost_fruits_and_veg"],
        "costs": Costs
    }

    print(f"[RESPONSE] {response}")
    return jsonify(response)


@app.route('/countries', methods=['GET'])
def countries():
    print("[REQUEST] /countries")
    return jsonify(predictor.list_countries())


@app.route('/continents', methods=['GET'])
def continents():
    print("[REQUEST] /continents")
    return jsonify(predictor.list_continents())


if __name__ == '__main__':
    print("Starting server")
    app.run(debug=True)