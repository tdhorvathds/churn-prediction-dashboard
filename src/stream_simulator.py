import time

from src.synthetic_generator import generate_customer_record
from src.storage import save_raw_record



def run_stream(interval_seconds: int = 30):
    print(f"Starting synthetic churn stream with {interval_seconds}s interval...")

    while True:
        record = generate_customer_record()
        save_raw_record(record)

        print(
            f"[{record['timestamp']}] Generated {record['customer_id']} "
            f"| city={record['city']} "
            f"| contract={record['contract_type']} "
            f"| monthly_charges={record['monthly_charges']}"
        )

        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_stream(interval_seconds=30)