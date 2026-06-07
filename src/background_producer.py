import argparse
import logging
import signal
import sys
import threading
import time

from src.synthetic_generator import generate_customer_record
from src.storage import save_raw_record
from src.config import LOG_DIR

LOG_FILE = LOG_DIR / "background_producer.log"


class BackgroundProducer:
    def __init__(self, interval_seconds: int = 60):
        self.interval_seconds = interval_seconds
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            logging.warning("Producer is already running.")
            return

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logging.info(
            "Background producer started with interval=%s seconds",
            self.interval_seconds,
        )

    def stop(self):
        logging.info("Stopping background producer...")
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logging.info("Background producer stopped.")

    def _run_loop(self):
        while not self._stop_event.is_set():
            try:
                record = generate_customer_record()
                save_raw_record(record)

                logging.info(
                    "Generated record customer_id=%s city=%s contract_type=%s monthly_charges=%s",
                    record["customer_id"],
                    record["city"],
                    record["contract_type"],
                    record["monthly_charges"],
                )
            except Exception:
                logging.exception("Producer iteration failed")

            interrupted = self._stop_event.wait(self.interval_seconds)
            if interrupted:
                break


def configure_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    parser = argparse.ArgumentParser(
        description="Run the synthetic churn background producer."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between generated records",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    configure_logging(verbose=args.verbose)

    producer = BackgroundProducer(interval_seconds=args.interval)

    def handle_shutdown(signum, frame):
        logging.info("Received shutdown signal: %s", signum)
        producer.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, handle_shutdown)

    producer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        producer.stop()


if __name__ == "__main__":
    main()