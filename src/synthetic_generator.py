import random
import pandas as pd
from datetime import datetime
from pathlib import Path

from src.schema import (
    CITIES,
    CONTRACT_TYPES,
    GENDERS,
    INTERNET_SERVICES,
    PAYMENT_METHODS,
)

RAW_STREAM_PATH = Path("data/raw/synthetic_stream.csv")

def get_next_customer_counter():
    if not RAW_STREAM_PATH.exists():
        return 1

    try:
        df = pd.read_csv(RAW_STREAM_PATH)

        if df.empty or "customer_id" not in df.columns:
            return 1

        last_customer_id = df.iloc[-1]["customer_id"]
        last_counter = int(str(last_customer_id).replace("CUST_", ""))
        return last_counter + 1

    except Exception:
        return 1


CUSTOMER_COUNTER = get_next_customer_counter()


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]



def generate_customer_record():
    global CUSTOMER_COUNTER

    customer_id = f"CUST_{CUSTOMER_COUNTER:06d}"
    CUSTOMER_COUNTER += 1

    timestamp = datetime.now().isoformat()

    gender = random.choice(GENDERS)
    city = weighted_choice(
        CITIES,
        [15, 10, 8, 12, 10, 10, 12, 8, 7, 8]
    )

    senior_citizen = random.choices([0, 1], weights=[0.84, 0.16])[0]
    partner = random.choices([0, 1], weights=[0.45, 0.55])[0]
    dependents = random.choices([0, 1], weights=[0.70, 0.30])[0]

    contract_type = weighted_choice(
        CONTRACT_TYPES,
        [0.55, 0.25, 0.20]
    )

    if contract_type == "Month-to-month":
        payment_method = weighted_choice(
            PAYMENT_METHODS,
            [0.50, 0.20, 0.15, 0.15]
        )
    else:
        payment_method = weighted_choice(
            PAYMENT_METHODS,
            [0.15, 0.10, 0.35, 0.40]
        )

    internet_service = weighted_choice(
        INTERNET_SERVICES,
        [0.35, 0.50, 0.15]
    )

    phone_service = random.choices([0, 1], weights=[0.10, 0.90])[0]

    if phone_service == 0:
        multiple_lines = 0
    else:
        multiple_lines = random.choices([0, 1], weights=[0.55, 0.45])[0]

    if internet_service == "No":
        online_security = 0
        online_backup = 0
        device_protection = 0
        tech_support = 0
        streaming_tv = 0
        streaming_movies = 0
    else:
        online_security = random.choices([0, 1], weights=[0.55, 0.45])[0]
        online_backup = random.choices([0, 1], weights=[0.50, 0.50])[0]
        device_protection = random.choices([0, 1], weights=[0.50, 0.50])[0]
        tech_support = random.choices([0, 1], weights=[0.60, 0.40])[0]
        streaming_tv = random.choices([0, 1], weights=[0.45, 0.55])[0]
        streaming_movies = random.choices([0, 1], weights=[0.45, 0.55])[0]

    if contract_type == "Month-to-month":
        tenure_months = random.randint(0, 24)
    elif contract_type == "One year":
        tenure_months = random.randint(12, 48)
    else:
        tenure_months = random.randint(24, 72)

    service_count = sum([
        phone_service,
        multiple_lines,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies,
    ])

    monthly_charges = 20

    if phone_service:
        monthly_charges += 20

    if internet_service == "DSL":
        monthly_charges += 25
    elif internet_service == "Fiber optic":
        monthly_charges += 45

    monthly_charges += service_count * random.uniform(4, 8)
    monthly_charges += random.uniform(-5, 5)

    monthly_charges = round(max(monthly_charges, 18.0), 2)

    noise_factor = random.uniform(0.90, 1.10)
    total_charges = round(
        tenure_months * monthly_charges * noise_factor,
        2,
    )

    record = {
        "timestamp": timestamp,
        "customer_id": customer_id,
        "senior_citizen": senior_citizen,
        "partner": partner,
        "dependents": dependents,
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "phone_service": phone_service,
        "multiple_lines": multiple_lines,
        "online_security": online_security,
        "online_backup": online_backup,
        "device_protection": device_protection,
        "tech_support": tech_support,
        "streaming_tv": streaming_tv,
        "streaming_movies": streaming_movies,
        "gender": gender,
        "city": city,
        "contract_type": contract_type,
        "payment_method": payment_method,
        "internet_service": internet_service,
    }

    return record