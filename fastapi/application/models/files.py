from sqlalchemy import Column, String, ForeignKey
from .base_model import BaseModel
from ..database import Base
from sqlalchemy.orm import relationship


class Signatures(BaseModel, Base):
    __tablename__ = "signatures"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    file_name = Column(String(50), nullable=False, unique=True)
    signatory_name = Column(String(30), ForeignKey('signatories.name'))
    signatory_id = Column(String(30), ForeignKey('signatories.id_no'))

class Signatory(BaseModel, Base):
    __tablename__ = "signatories"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    name = Column(String(50), nullable=False, unique=True)
    id_no = Column(String(11), nullable=False, unique=True)
    signatures = relationship(
        "Signatures",
        backref="signatory",
        foreign_keys=[Signatures.signatory_name]  # You can specify either signatory_name or signatory_id
    )
    account_no = Column(String(50), ForeignKey('corporate_accounts.account_no'))

class AccountDocuments(BaseModel):
    name = Column(String(40), nullable=False)
    doc_type = Column(String(40), nullable=False)

class CorporateDocs(AccountDocuments, Base):
    __tablename__ = "corporate_documents"
    account_no = Column(String(50), ForeignKey('corporate_accounts.account_no'))

class PersonalDocs(AccountDocuments, Base):
    __tablename__ = "personal_documents"
    account_no = Column(String(50), ForeignKey('personal_accounts.account_no'))

class F_C_A_Docs(AccountDocuments, Base):
    __tablename__ = "fca_documents"
    account_no = Column(String(50), ForeignKey('foreign_currency_accounts.account_no'))