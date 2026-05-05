# Food Price Predictor

Food Price Predictor is a local web app for analyzing food price data and running a prediction backend.

## Requirements

- Python 3
- Node.js and npm

## Setup

1. Download all files and open a terminal in the project folder.

2. Create and activate the virtual environment (macOS / Linux):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies if needed:
    ```bash
   
    pip install flask flask-cors

    # For Mac/Linux  - source venv/bin/activate 
    pip install flask flask-cors

    pip install numpy
    pip install pandas
    pip install scikit-learn
   ```

4. Install frontend dependencies:

   ```bash
   npm install
   ```

## Running the app

### Backend

In terminal 1 in your project folder:

```bash
source .venv/bin/activate
python3 Backend.py
```

### Frontend

In terminal 2 in your project folder:

```bash
npm start
```

Then open http://localhost:3000 in your browser.

## Notes

- If the virtual environment is already created, use `source .venv/bin/activate` before running the backend.
- If you are on Windows, activate the virtual environment with:

  ```powershell
  .venv\Scripts\activate
  ```
- To run the juypter notebooks and graphs in notebooks
   ```bash
   pip install matplotlib jupyter
   ```
