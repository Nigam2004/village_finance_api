
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# load_dotenv()  # Load DATABASE_URL from the project's .env file


DATABASE_URL = "postgresql+psycopg://postgres:12345@localhost:5432/village_finance"


engine = create_engine(DATABASE_URL)
print("Database connection created")

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine )


Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#test connection
def test_db():  
    try:
        with engine.connect() as connection:
            print('db connected succesfully')
    except Exception as err:
        print("Connection failed:", err)
