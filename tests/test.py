import random

from src.data_loader import load_model_features

df = load_model_features()
row = df[df["customer_id"] == "7590-VHVEG"].iloc[0]

# print(row.to_dict())

senior_citizen = random.choices([0, 1], weights=[0.84, 0.16])[0]
print(senior_citizen)
