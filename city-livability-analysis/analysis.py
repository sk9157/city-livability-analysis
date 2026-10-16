import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/city_data.csv")

def normalize_lower_better(series):
    return (series.max() - series) / (series.max() - series.min()) * 100


def normalize_higher_better(series):
    return (series - series.min()) / (series.max() - series.min()) * 100


def normalize_ideal(series, ideal=72):
    distance = (series - ideal).abs()
    max_distance = distance.max()
    return (1 - distance / max_distance) * 100


df["SafetyScore"] = normalize_lower_better(df["CrimeRate"])
df["IncomeScore"] = normalize_higher_better(df["MedianIncome"])
df["CostScore"] = normalize_lower_better(df["AverageRent"])
df["WeatherScore"] = normalize_ideal(df["AverageTemperature"])
df["JobScore"] = normalize_lower_better(df["UnemploymentRate"])
df["TransportScore"] = normalize_higher_better(df["Walkability"])
df["HealthcareScore"] = normalize_higher_better(df["HospitalBeds"])
df["EntertainmentScore"] = normalize_higher_better(df["UrbanActivity"])

weights = {
    "SafetyScore": 0.20,
    "IncomeScore": 0.15,
    "CostScore": 0.20,
    "WeatherScore": 0.10,
    "JobScore": 0.15,
    "TransportScore": 0.08,
    "HealthcareScore": 0.07,
    "EntertainmentScore": 0.05,
}

assert abs(sum(weights.values()) - 1.0) < 1e-9, "Weights must sum to 1."


df["LivabilityScore"] = 0.0

score_columns = list(weights.keys())

for column in score_columns:
    assert df[column].between(0, 100).all(), f"{column} contains invalid scores."


for score_column, weight in weights.items():
    df["LivabilityScore"] += df[score_column] * weight

ranked = df.sort_values("LivabilityScore", ascending=False)

ranked[["City", "LivabilityScore"]].to_csv(
    "output/city_rankings.csv",
    index=False
)

print(ranked[["City", "LivabilityScore"]])


ranked_plot = ranked.sort_values("LivabilityScore")

plt.figure(figsize=(10, 6))

plt.barh(
    ranked_plot["City"],
    ranked_plot["LivabilityScore"]
)

plt.xlabel("Livability Score")
plt.ylabel("City")
plt.title("Overall Livability Ranking")

plt.tight_layout()
plt.savefig("output/city_rankings.png", dpi=300)
plt.show()

