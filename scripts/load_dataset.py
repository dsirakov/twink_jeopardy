import csv
import logging
from datetime import datetime
from app.db.session import engine, SessionLocal, Base
from app.db.models import Question

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Starting dataset loading...")
Base.metadata.create_all(engine)
db = SessionLocal()

loaded_count = 0
skipped_count = 0

logger.info("Loading dataset from data/JEOPARDY_CSV.csv...")
with open("data/JEOPARDY_CSV.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        value = row[" Value"].replace("$", "").strip()
        if not value.isdigit():
            skipped_count += 1
            continue

        value = int(value)
        if value > 1200:
            skipped_count += 1
            continue

        q = Question(
            show_number=int(row["Show Number"]),
            air_date=datetime.strptime(row[" Air Date"], "%Y-%m-%d").date(),
            round=row[" Round"],
            category=row[" Category"],
            value=value,
            question=row[" Question"],
            answer=row[" Answer"],
        )
        db.add(q)
        loaded_count += 1


db.commit()
db.close()

logger.info(
    f"Dataset loading complete! Loaded {loaded_count} questions, skipped {skipped_count} rows."
)
