from .base_model import BaseModel
from ..database import Base
from sqlalchemy import Column, Text, Integer, ForeignKey, Boolean


class ClientHelpRequest(BaseModel, Base):
    __tablename__ = "client_help"
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

class ClientReports(BaseModel, Base):
    __tablename__ = "client_reports"
    owner_customer_no = Column(Integer, ForeignKey('customers.customer_no'))
    text = Column(Text, nullable=False)
    status_resolved = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"{self.id}"