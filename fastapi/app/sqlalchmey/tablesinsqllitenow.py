from sqlalchemy import inspect, create_engine

engine = create_engine("sqlite:///test.db", echo=True)
inspector = inspect(engine)

tables = inspector.get_table_names()
print(f"Total tables: {len(tables)}")

for table in tables:
    print(f"\nTable: {table}")
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")