import csv
from datetime import datetime
from app.db.session import engine, SessionLocal, Base
from app.db.models import Question

Base.metadata.create_all(engine)
db = SessionLocal()

with open("data/JEOPARDY_CSV.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        value = row[" Value"].replace("$", "").strip()
        if not value.isdigit():
            continue

        value = int(value)
        if value > 1200:
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

db.commit()
db.close()
