from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, Session

# Connect to your existing SQLite database
engine = create_engine('sqlite:///MyTreeDatabase.db')

# Create a base class for declarative models
Base = declarative_base()

# Define the Tree model
class Tree(Base):
    __tablename__ = 'tree'

    id = Column(Integer, primary_key=True)
    species = Column(String(255))
    meters = Column(Float)
    feet = Column(Float)
    category = Column(String(255))

    def __repr__(self):
        return f"<Tree(id={self.id}, species='{self.species}', height={self.meters}m / {self.feet}ft)>"

# Create a metadata object to represent the database schema
metadata = MetaData()

# Reflect the database schema into Python objects
metadata.reflect(bind=engine)

# Get the 'tree' table
tree_table = metadata.tables['tree']

# Create a session to interact with the database
with Session(engine) as session:
    # Query the database
    results = session.query(tree_table).all()

    # Print the results
    print("All rows from 'tree' table:")
    for row in results:
        print(f"ID: {row.id}, Species: {row.species}, Height: {row.meters}m / {row.feet}ft")


# with Session(engine) as session:
#     # Create a new Tree object
#     new_tree = Tree(
#         species="Giant Sequoia (Sequoiadendron giganteum)",
#         Meters=95.7,
#         Feet=314.0
#     )

#     # Add the new tree to the session
#     session.add(new_tree)

#     # Commit the transaction
#     session.commit()

#     print(f"Added new tree: {new_tree}")