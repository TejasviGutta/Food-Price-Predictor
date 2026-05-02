import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

TARGETS = ["annual_cost_healthy_diet", "annual_total_food_cost", "annual_cost_fruits_and_veg"]


class FoodCostPredictor:

    def __init__(self, csv_path="FP_output.csv"):
        self._df = self._load(csv_path)
        self._build_cpi_table()
        self._build_ohe()
        self._train()
        self._fit_trend_models()


    def _load(self, path):
        df = pd.read_csv(path)
        df = df.rename(columns={
            "cost_healthy_diet_ppp_usd":    "daily_cost",
            "annual_cost_healthy_diet_usd": "annual_cost_healthy_diet",
            "cost_vegetables_ppp_usd":      "cost_veg",
            "cost_fruits_ppp_usd":          "cost_fruit",
        })
        df["year"] = df["year"].astype(int)
        df["continent"] = df["continent"].fillna("Unknown")

        df["cpi_pct"] = np.where(df["cpi"].abs() < 50, df["cpi"], np.nan)
        df = df.groupby(["country", "year"]).agg({
            "continent": "first", "daily_cost": "first",
            "annual_cost_healthy_diet": "first", "cost_veg": "first",
            "cost_fruit": "first", "total_food_components_cost": "first",
            "cpi_pct": "mean",
        }).reset_index().sort_values(["country", "year"]).reset_index(drop=True)

        df["annual_cost_healthy_diet"] = df["annual_cost_healthy_diet"]

        r_total = self._ratio(df, "total_food_components_cost", "daily_cost")
        df["annual_total_food_cost"] = np.where(
            df["total_food_components_cost"].notna(),
            df["total_food_components_cost"] * 365,
            df["daily_cost"] * r_total * 365,
        )

        df["fv"] = df["cost_fruit"].fillna(0) + df["cost_veg"].fillna(0)
        r_fv = self._ratio(df, "fv", "daily_cost", require="cost_fruit")
        df["annual_cost_fruits_and_veg"] = np.where(
            df["cost_fruit"].notna(),
            df["fv"] * 365,
            df["daily_cost"] * r_fv * 365,
        )

        df["lag1"] = df.groupby("country")["annual_cost_healthy_diet"].shift(1)
        df["lag2"] = df.groupby("country")["annual_cost_healthy_diet"].shift(2)
        mean_by_country = df.groupby("country")["annual_cost_healthy_diet"].transform("mean")
        df["lag1"] = df["lag1"].fillna(mean_by_country)
        df["lag2"] = df["lag2"].fillna(mean_by_country)

        self._year_min = int(df["year"].min())
        self._year_max = int(df["year"].max())
        return df

    @staticmethod
    def _ratio(df, num, den, require=None):
        mask = df[num].notna() & df[den].notna()
        if require:
            mask &= df[require].notna()
        s = df.loc[mask]
        return float((s[num] / s[den].replace(0, np.nan)).median()) if not s.empty else 1.0

    # CPI table
    
    def _build_cpi_table(self):
        g = self._df.groupby("year")["cpi_pct"].mean().dropna()
        self._cpi_global   = dict(g)
        self._baseline_cpi = float(g.mean())
        self._cpi_country = (
            self._df.dropna(subset=["cpi_pct"])
            .groupby(["country", "year"])["cpi_pct"].mean()
            .unstack("year").to_dict(orient="index")
        )
        from sklearn.linear_model import Ridge
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.pipeline import Pipeline
        X = (g.index.values - g.index.min()).reshape(-1, 1)
        self._cpi_trend = Pipeline([("p", PolynomialFeatures(1)), ("r", Ridge())])
        self._cpi_trend.fit(X, g.values)
        self._cpi_base_yr = int(g.index.min())

    def _get_cpi(self, year, country=None):
        if country and country in self._cpi_country:
            v = self._cpi_country[country].get(year)
            if v is not None and not np.isnan(float(v)):
                return float(v)
        if year in self._cpi_global:
            return float(self._cpi_global[year])
        return float(self._cpi_trend.predict([[year - self._cpi_base_yr]])[0])

    # One-hot encoding

    def _build_ohe(self):
        self._countries  = sorted(self._df["country"].unique())
        self._continents = sorted(self._df["continent"].unique())

    def _ohe(self, country, continent):
        c  = [1.0 if x == country   else 0.0 for x in self._countries]
        ct = [1.0 if x == continent else 0.0 for x in self._continents]
        return np.array(c + ct)

    # Train 

    def _make_X(self, df):
        numeric = df[["year_norm", "cpi_change_pct", "lag1", "lag2"]].values
        ohe     = np.vstack([self._ohe(r["country"], r["continent"]) for _, r in df.iterrows()])
        return np.hstack([numeric, ohe])

    def _train(self):
        df = self._df.copy()
        df["cpi_change_pct"] = df["year"].map(self._cpi_global)
        df = df.dropna(subset=["cpi_change_pct"]).copy()
        df["year_norm"] = df["year"] - self._year_min
        X = self._make_X(df)

        self._models = {}
        for t in TARGETS:
            X_tr, X_te, y_tr, y_te = train_test_split(X, df[t].values, test_size=0.2, random_state=42)
            reg = GradientBoostingRegressor(n_estimators=300, max_depth=4,
                                            learning_rate=0.05, subsample=0.8,
                                            min_samples_leaf=5, random_state=42)
            reg.fit(X_tr, y_tr)
            self._models[t] = reg
            print(f"  {t}: R² = {r2_score(y_te, reg.predict(X_te)):.3f}")

        last = df.sort_values("year").groupby("country").last()
        self._last = last[["lag1", "lag2"]].to_dict(orient="index")

    # Trend models

    def _fit_trend_models(self):
        def cagr(series):
            s = series.dropna()
            if len(s) < 2 or s.iloc[0] <= 0: return 0.05
            return (s.iloc[-1] / s.iloc[0]) ** (1 / (len(s) - 1)) - 1

        df = self._df
        self._cagr_global    = {t: cagr(df.groupby("year")[t].mean()) for t in TARGETS}
        self._anchor_global  = df.groupby("year")[TARGETS].mean().iloc[-1].to_dict()
        self._cagr_country   = {c: {t: cagr(g.set_index("year")[t]) for t in TARGETS}
                                 for c, g in df.groupby("country")}
        self._anchor_country = {c: g.sort_values("year")[TARGETS].iloc[-1].to_dict()
                                 for c, g in df.groupby("country")}
        self._cagr_continent  = {c: {t: cagr(g.groupby("year")[t].mean()) for t in TARGETS}
                                  for c, g in df.groupby("continent")}
        self._anchor_continent = {c: g.groupby("year")[TARGETS].mean().iloc[-1].to_dict()
                                   for c, g in df.groupby("continent")}

    # Predict

    def predict(self, year, country=None, continent=None, cpi_change=None):
        if country and country not in self._countries:
            raise ValueError(f"Unknown country '{country}'. Use list_countries().")
        if continent and not country and continent not in self._continents:
            raise ValueError(f"Unknown continent '{continent}'. Use list_continents().")

        cpi = cpi_change if cpi_change is not None else self._get_cpi(year, country)

        if year <= self._year_max:
            vals = self._gbr_predict(year, country, continent, cpi)
        else:
            vals = self._trend_predict(year, country, continent, cpi)

        return {
            "year": year,
            "scope": f"country: {country}" if country else f"continent: {continent}" if continent else "global",
            "annual_cost_healthy_diet":   float(round(vals["annual_cost_healthy_diet"], 2)),
            "annual_total_food_cost":     float(round(vals["annual_total_food_cost"], 2)),
            "annual_cost_fruits_and_veg": float(round(vals["annual_cost_fruits_and_veg"], 2)),
            "cpi_change_used": float(round(cpi, 2)),
            "extrapolation": year > self._year_max,
        }

    def _row_X(self, country, continent, year_norm, cpi, lag1, lag2):
        num = np.array([[year_norm, cpi, lag1, lag2]])
        return np.hstack([num, self._ohe(country, continent).reshape(1, -1)])

    def _gbr_predict(self, year, country, continent, cpi):
        yn = year - self._year_min
        if country:
            cont = self._df.loc[self._df["country"] == country, "continent"].iloc[0]
            lags = self._last.get(country, {"lag1": 0, "lag2": 0})
            X    = self._row_X(country, cont, yn, cpi, lags["lag1"], lags["lag2"])
            return {t: float(self._models[t].predict(X)[0]) for t in TARGETS}

        scope = (self._df.loc[self._df["continent"] == continent, "country"].unique()
                 if continent else self._df["country"].unique())
        rows = []
        for c in scope:
            cont = self._df.loc[self._df["country"] == c, "continent"].iloc[0]
            lags = self._last.get(c, {"lag1": 0, "lag2": 0})
            X    = self._row_X(c, cont, yn, cpi, lags["lag1"], lags["lag2"])
            rows.append({t: float(self._models[t].predict(X)[0]) for t in TARGETS})
        return {t: float(np.mean([r[t] for r in rows])) for t in TARGETS}

    def _trend_predict(self, year, country, continent, cpi):
        if country:
            cagr, anchor = self._cagr_country[country], self._anchor_country[country]
        elif continent:
            cagr, anchor = self._cagr_continent[continent], self._anchor_continent[continent]
        else:
            cagr, anchor = self._cagr_global, self._anchor_global

        years_ahead = year - self._year_max
        cpi_factor  = (max(abs(cpi), 0.1) / max(self._baseline_cpi, 0.5)) ** 0.5
        return {
            t: anchor[t] * ((1 + np.clip(cagr[t] * cpi_factor, 0.005, 0.15)) ** years_ahead)
            for t in TARGETS
        }

    # Helpers
    def list_countries(self):
        return sorted(self._countries)

    def list_continents(self):
        return sorted(self._continents)

    def get_historical(self, country=None, continent=None):
        df = self._df.copy()
        if country:   df = df[df["country"] == country]
        if continent: df = df[df["continent"] == continent]
        return df[["country", "continent", "year"] + TARGETS].sort_values(["country", "year"])


# Testing
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year",       type=int)
    parser.add_argument("--country",    type=str)
    parser.add_argument("--continent",  type=str)
    parser.add_argument("--cpi_change", type=float)
    parser.add_argument("--csv",        type=str, default="foodprices_output.csv")
    parser.add_argument("--list",       action="store_true")
    args = parser.parse_args()

    model = FoodCostPredictor(args.csv)

    if args.list:
        print("Countries :", model.list_countries())
        print("Continents:", model.list_continents())
    elif args.year:
        r = model.predict(args.year, args.country, args.continent, args.cpi_change)
        warn = "  ⚠ extrapolation" if r["extrapolation"] else ""
        print(f"\n  Year   : {r['year']}  [{r['scope']}]{warn}")
        print(f"  CPI    : {r['cpi_change_used']:.2f}%")
        print(f"  Healthy diet cost      : ${r['annual_cost_healthy_diet']:>14,.2f}")
        print(f"  Total food cost        : ${r['annual_total_food_cost']:>14,.2f}")
        print(f"  Fruits & veg cost      : ${r['annual_cost_fruits_and_veg']:>14,.2f}\n")
    else:
        print(f"Loaded — {len(model.list_countries())} countries, {len(model.list_continents())} continents")
        while True:
            try:
                yr  = input("Year: ").strip()
                co  = input("Country  (blank=global): ").strip() or None
                cnt = input("Continent (blank=skip) : ").strip() or None if not co else None
                cpi = input("CPI % (blank=auto)     : ").strip()
                r = model.predict(int(yr), co, cnt, float(cpi) if cpi else None)
                warn = "  ⚠ extrapolation" if r["extrapolation"] else ""
                print(f"\n  Year   : {r['year']}  [{r['scope']}]{warn}")
                print(f"  CPI    : {r['cpi_change_used']:.2f}%")
                print(f"  Healthy diet cost      : ${r['annual_cost_healthy_diet']:>14,.2f}")
                print(f"  Total food cost        : ${r['annual_total_food_cost']:>14,.2f}")
                print(f"  Fruits & veg cost      : ${r['annual_cost_fruits_and_veg']:>14,.2f}\n")
            except (ValueError, KeyboardInterrupt) as e:
                if isinstance(e, KeyboardInterrupt): break
                print(f"Error: {e}")