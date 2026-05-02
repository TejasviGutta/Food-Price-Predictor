# Food Price Predictor

Food Price Predictor is a local web app for analyzing food price data and running a prediction backend.

## Requirements

- Python 3
- Node.js and npm

## Setup

1. Open a terminal in the project folder:

   ```bash
   cd /Users/sahitithopucherla/Documents/Food-Price-Predictor
   ```

2. Create and activate the virtual environment (macOS / Linux):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies if needed.

4. Install frontend dependencies:

   ```bash
   npm install
   ```

## Running the app

### Backend

In terminal 1:

```bash
cd /Users/sahitithopucherla/Documents/Food-Price-Predictor
source .venv/bin/activate
python3 Backend.py
```

### Frontend

In terminal 2:

```bash
cd /Users/sahitithopucherla/Documents/Food-Price-Predictor
npm start
```

Then open http://localhost:3000 in your browser.

## Notes

- If the virtual environment is already created, use `source .venv/bin/activate` before running the backend.
- If you are on Windows, activate the virtual environment with:

  ```powershell
  .venv\Scripts\activate
  ```
