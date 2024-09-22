from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from database.entities import init_db
# Define the PostgreSQL database connection string
DATABASE_URL = "postgresql://pdf_chat_user:5uperSecr3tP%40ssw0rd!@localhost:5432/pdf_chat"

# Create the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_and_init_db():
    inspector = inspect(engine)

    # Check if all the defined tables exist
    tables = ['user', 'document', 'embedding', 'chat', 'message']
    existing_tables = inspector.get_table_names()

    missing_tables = [table for table in tables if table not in existing_tables]

    if missing_tables:
        print(f"Missing tables: {', '.join(missing_tables)}. Creating tables...")
        init_db(engine)
    else:
        print("All tables already exist, no need to create tables.")

# Call the function to check and initialize the database if needed
if __name__ == "__main__":
    check_and_init_db()