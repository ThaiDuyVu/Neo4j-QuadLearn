"""CLI cross-platform: python -m scripts.db init|check|queries|annotate|reset --yes."""
import argparse
from app.core.config import ROOT, Settings
from app.core.database import Database
from app.shared.utils.cypher import statements

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "check", "queries", "annotate", "reset"])
    parser.add_argument("--yes", action="store_true", help="Xác nhận xóa node có demo=true")
    args = parser.parse_args()
    settings = Settings.load()
    if args.command == "reset" and (not args.yes or settings.app_env != "development"):
        parser.error("Reset chỉ cho APP_ENV=development và phải thêm --yes.")
    db = Database(settings)
    try:
        db.verify()
        if args.command == "check":
            print("Neo4j connection OK")
        elif args.command == "queries":
            for query in statements(ROOT / "database/examples.cypher"):
                print(db.read(query))
        elif args.command == "annotate":
            db.apply(statements(ROOT / "database/taxonomy_conditions.cypher"))
            print("Đã cập nhật chú thích điều kiện trên các quan hệ IS_A hiện có")
        else:
            if args.command == "reset":
                db.apply(statements(ROOT / "database/reset_dev.cypher"))
            for name in ("constraints.cypher", "indexes.cypher", "seed.cypher", "taxonomy_conditions.cypher"):
                db.apply(statements(ROOT / "database" / name))
            print("Constraints, indexes và seed OK")
    finally:
        db.close()

if __name__ == "__main__":
    main()
