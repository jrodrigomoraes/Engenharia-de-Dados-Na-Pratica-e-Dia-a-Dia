import sqlalchemy

def save_to_database(df):
    engine = sqlalchemy.create_engine("postgresql://user:password@localhost/dbname")
    df.to_sql('usuarios', con=engine, if_exists='replace', index=False)