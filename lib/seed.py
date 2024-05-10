from faker import Faker
from model import Specialist, Patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Create a Faker instance
fake = Faker()

# Define function to generate fake data for specialists
# Define function to generate fake data for specialists
# Define function to generate fake data for specialists
# Define function to generate fake data for specialists
def generate_specialist_data():
    return {
        'age': fake.random_int(min=25, max=70),
        'specialization': fake.random_element(elements=('Cardiologist', 'General Doctor', 'Nurse'))
    }


# Define function to generate fake data for patients
def generate_patient_data():
    return {
        'Age': fake.random_int(min=10, max=90),
        'Sex': fake.random_element(elements=('male', 'female')),
        'ChestPainType': fake.random_element(elements=('ATA', 'NAP', 'ASY')),
        'RestingBP': f"{fake.random_int(min=90, max=180)}/{fake.random_int(min=60, max=120)}",
        'Cholesterol': fake.random_int(min=100, max=300),
        'FastingBS': fake.boolean(),
        'ecg': fake.random_element(elements=('Normal', 'Abnormal')),
        'MaxHR': fake.random_int(min=60, max=200),
        'ExerciseAngina': fake.random_element(elements=('Y', 'N')),
        'Oldpeak': fake.random_int(min=0, max=5),
        'segment_slope': fake.random_element(elements=('Up', 'Flat', 'Down')),
        'HeartDisease': fake.boolean()
    }


# Create engine and session
DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Generate and insert fake data for specialists
for _ in range(200):  # Generate 200 specialists
    specialist_data = generate_specialist_data()
    specialist = Specialist(**specialist_data)
    session.add(specialist)

# Generate and insert fake data for patients
for _ in range(400):  # Generate 400 patients
    patient_data = generate_patient_data()
    patient = Patient(data=patient_data)
    session.add(patient)

# Commit the changes
session.commit()

def export_specialist_data_to_excel():
    # Query specialist data from database
    query = "SELECT * FROM specialists"
    specialist_df = pd.read_sql(query, engine)

    # Export specialist data to Excel
    specialist_df.to_excel("specialist_data.xlsx", index=False)

# Define function to export patient data to Excel
def export_patient_data_to_excel():
    # Query patient data from database
    query = "SELECT * FROM patients"
    patient_df = pd.read_sql(query, engine)

    # Export patient data to Excel
    patient_df.to_excel("patient_data.xlsx", index=False)

# Call the functions to export data
export_specialist_data_to_excel()
export_patient_data_to_excel()
