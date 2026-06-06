import os
import pandas as pd
import matplotlib.pyplot as plt


# load dataset
path = r"C:\Users\Overnight\OneDrive - THE SALVATION ARMY CANADA AND BERMUDA\Desktop\archive\airline.parquet\year=1988\day_of_week=Friday"
df = pd.read_parquet(path)

# standardize column names
df.columns = df.columns.str.lower()

# convert delay columns to numeric
df["departure_delay"] = pd.to_numeric(df["departure_delay"], errors="coerce")
df["arrival_delay"] = pd.to_numeric(df["arrival_delay"], errors="coerce")

# remove missing values
df = df.dropna(subset=["departure_delay", "arrival_delay"])

# feature engineering
df["total_delay"] = df["departure_delay"] + df["arrival_delay"]

# aggregation
carrier_delay = df.groupby("unique_carrier")["total_delay"].mean()

print("\nAverage Delay by Carrier:\n")
print(carrier_delay)

# sort for better insight
carrier_delay_sorted = carrier_delay.sort_values(ascending=False)

# visualization
carrier_delay_sorted.plot(kind="bar")
plt.title("Average Flight Delay by Carrier (1987)")
plt.xlabel("Carrier")
plt.ylabel("Average Delay (minutes)")
plt.tight_layout()

plt.savefig("visuals/carrier_delay.png")
plt.show()

# insights (safe check)
if not carrier_delay.empty:
    print("\nMost reliable carrier:", carrier_delay.idxmin())
    print("Worst carrier:", carrier_delay.idxmax())