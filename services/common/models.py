from sqlalchemy import Column, Integer, String, Double, Float, DateTime, func

from services.common.db import Base


class Customer(Base):
    """
    Модель клиента
    """

    __tablename__ = "customers"
    customerID = Column(String(50), primary_key=True)
    gender = Column(String(20))
    SeniorCitizen = Column(Integer)
    Partner = Column(String(10))
    Dependents = Column(String(10))
    tenure = Column(Integer)
    PhoneService = Column(String(30))
    MultipleLines = Column(String(30))
    InternetService = Column(String(30))
    OnlineSecurity = Column(String(30))
    OnlineBackup = Column(String(30))
    DeviceProtection = Column(String(30))
    TechSupport = Column(String(30))
    StreamingTV = Column(String(30))
    StreamingMovies = Column(String(30))
    Contract = Column(String(50))
    PaperlessBilling = Column(String(10))
    PaymentMethod = Column(String(50))
    MonthlyCharges = Column(Double)
    TotalCharges = Column(Double)

class Prediction(Base):
    """
    Модель предсказаний
    """

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), nullable=False)
    risk = Column(String(20), nullable=False)
    probability = Column(Float, nullable=False)
    prediction = Column(String(20), nullable=False)
    threshold = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())
