from src.data_loader import load_model_features

df = load_model_features()
row = df[df["customer_id"] == "7590-VHVEG"].iloc[0]

print(row.to_dict())