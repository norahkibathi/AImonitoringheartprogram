#the purpose of the code is to allow users to manage a system that allows users to monitor their heart failure risk
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import Flask
Base = declarative_base()


  
Base = declarative_base()


class Specialist(Base):
    __tablename__ = 'specialists'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    specialization = Column(String)
    patients_assigned = relationship("Patient", back_populates="assigned_specialist", overlaps="patients_assigned")

    def __init__(self, age, specialization):  # Update constructor parameters accordingly
        self.age = age
        self.specialization = specialization


    def consult(self, patient):
        if patient.risk_category.startswith("HIGH RISK"):
            return f"Cardiologist {self.id} is ready to consult with {patient.id}."
        elif patient.risk_category.startswith("MODERATE RISK"):
            return f"General Doctor {self.id} is ready to consult with {patient.id}."
        elif patient.risk_category.startswith("LOW RISK"):
            return f"Nurse {self.id}  will assist {patient.id}."



class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    sex = Column(String)
    chest_pain_type = Column(String)  # Renamed for clarity
    resting_bp = Column(String)  # Assuming RestingBP is a string (e.g., "140/90")
    cholesterol = Column(Integer)  # Assuming Cholesterol is numerical
    fasting_bs = Column(Boolean)  # Assuming FastingBS is 0 or 1 (boolean)
    ecg = Column(String)
    max_hr = Column(Integer)  # Assuming MaxHR is numerical
    exercise_angina = Column(String)  # Assuming ExerciseAngina is string ("Y" or "N")
    oldpeak = Column(Float)  # Assuming Oldpeak is numerical
    segment_slope = Column(String)
    heart_disease = Column(Boolean)  # Assuming HeartDisease is 0 or 1 (boolean)
    risk_score = Column(Integer)
    risk_category = Column(String)
    specialist_id = Column(Integer, ForeignKey('specialists.id'))
    assigned_specialist = relationship("Specialist", back_populates="patients_assigned", overlaps="assigned_doctor")
    ecg_results = Column(String)  # New column for ECG results

    def __init__(self, data):
        # Assuming data is a dictionary with keys matching the column names

        self.age = data['Age']
        self.sex = data['Sex']
        self.chest_pain_type = data['ChestPainType']
        self.resting_bp = data['RestingBP']
        self.cholesterol = data['Cholesterol']
        self.fasting_bs = bool(data['FastingBS'])  # Convert to boolean (0 or 1)
        self.ecg = data['ecg']
        self.max_hr = data['MaxHR']
        self.exercise_angina = data['ExerciseAngina']
        self.oldpeak = data['Oldpeak']
        self.segment_slope = data['ST_Slope']
        self.heart_disease = bool(data['HeartDisease'])  # Convert to boolean (0 or 1)
        self.ecg_results = data.get('ECGResults')  # Set ECG results if available
        self.calculate_risk_score()
        self.get_risk_category()

    def calculate_risk_score(self):

        self.risk_score = int(self.age >= 65)  # Adjust based on your risk factors

        # Add points based on chest pain type (consider medical guidance for weightage)
        if self.chest_pain_type == "ATA":
            self.risk_score += 2  # Adjust weight as needed
        elif self.chest_pain_type in ("NAP", "ASY"):
            self.risk_score += 1  # Adjust weight as needed

        # Add points based on resting blood pressure
        if self.resting_bp:
            try:
                systolic, diastolic = map(int, self.resting_bp.split("/"))
                if systolic >= 140 or diastolic >= 90:
                    self.risk_score += 2  # Adjust weight as needed
            except ValueError:
                pass  # Ignore invalid blood pressure format

        # Add points based on other factors (refer to medical resources for weightage)
       
        # Adjust based on cholesterol level (consider thresholds and weightage)
        if self.cholesterol and self.cholesterol >= 240:  # Assuming cholesterol level is in mg/dL
            self.risk_score += 1

        # Adjust based on heart rate (consider thresholds and weightage based on Sex)
        if self.max_hr:
            if self.sex == "Male" and self.max_hr > 100:
                self.risk_score += 1
            elif self.sex == "Female" and self.max_hr > 90:
                self.risk_score += 1

        # Adjust based on ECG results
        if self.ecg_results == "Abnormal":
            self.risk_score += 1

        self.get_risk_category()



    
#enables direction whether to visit an expert or not
    def get_risk_category(self):
       if self.risk_score >= 4:
            self.risk_category = "HIGH RISK: Please consult a cardiologist for further evaluation and management."
       elif self.risk_score >= 2:
            self.risk_category = "MODERATE RISK: Consider lifestyle modifications and consult a general doctor for advice."
       else:
            self.risk_category = "LOW RISK: Maintain healthy habits and schedule regular checkups."


DATABASE_URL = 'sqlite:///heart.db'
# Define your classes (Specialist and Patient) here...

# Create engine and session
DATABASE_URL = 'sqlite:///heart.db'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Close the session
session.close()




