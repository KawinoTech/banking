"""
Document Management Module.

This module provides models for managing various types of documents and signatures associated with accounts and 
loans in the system. It defines relationships between signatories, signatures, and different categories of documents.

Models:
    - Signatures: Represents electronic or scanned signatures linked to signatories.
    - Signatory: Represents a person authorized to sign, linked to one or more signatures and associated with an account.
    - AccountDocuments (Base Class): A base class for various account-related document models, offering common attributes.
    - CorporateDocs: Represents corporate account documents.
    - PersonalDocs: Represents personal account documents.
    - F_C_A_Docs: Represents foreign currency account documents.
    - LoanDocs: Represents loan-related documents.
    - MortgageDocs: Represents mortgage-related documents.

Relationships:
    - A `Signatory` is linked to multiple `Signatures` via the `signatures` relationship.
    - All document models inherit from `AccountDocuments` for consistent schema design.

Table Names:
    - signatures: Stores signature files linked to signatories.
    - signatories: Stores details of individuals authorized to sign.
    - corporate_documents: Stores documents related to corporate accounts.
    - personal_documents: Stores documents related to personal accounts.
    - fca_documents: Stores documents related to foreign currency accounts.
    - loan_documents: Stores documents related to business loans.
    - mortgage_documents: Stores documents related to mortgages.

Attributes:
    - file_name (Signatures): Unique file name for the stored signature.
    - signatory_name and signatory_id (Signatures): Foreign keys referencing the name and ID of the associated signatory.
    - name and id_no (Signatory): Unique name and identification number of the signatory.
    - signatures (Signatory): Relationship linking signatory to multiple signatures.
    - account_no (Docs): Links each document to the relevant account, loan, or mortgage.

Usage:
    - Useful in workflows involving document generation, validation, or storage for customer accounts.
    - Supports relationships for retrieving and associating related data efficiently.
"""

from sqlalchemy import Column, String, ForeignKey
from .base_model import BaseModel
from . import Base
from sqlalchemy.orm import relationship


class Signatures(BaseModel, Base):
    """
    Represents an electronic or scanned signature linked to a signatory.

    Attributes:
        file_name (String): A unique file name for the signature (required, unique).
        signatory_name (String): Foreign key referencing the `name` of the signatory.
        signatory_id (String): Foreign key referencing the `id_no` of the signatory.
    """
    __tablename__ = "signatures"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    file_name = Column(String(50), nullable=False, unique=True)
    signatory_name = Column(String(30), ForeignKey('signatories.name'))
    signatory_id = Column(String(30), ForeignKey('signatories.id_no'))


class Signatory(BaseModel, Base):
    """
    Represents a signatory, an individual authorized to sign documents.

    Attributes:
        name (String): The unique name of the signatory (required, unique).
        id_no (String): The unique identification number of the signatory (required, unique).
        signatures (relationship): Relationship linking the signatory to multiple `Signatures`.
        account_no (String): Foreign key linking the signatory to a corporate account.
    """
    __tablename__ = "signatories"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    name = Column(String(50), nullable=False, unique=True)
    id_no = Column(String(11), nullable=False, unique=True)
    signatures = relationship(
        "Signatures",
        backref="signatory",
        foreign_keys=[Signatures.signatory_name]
    )
    account_no = Column(String(50), ForeignKey('corporate_accounts.account_no'))


class AccountDocuments(BaseModel):
    """
    Base class representing common attributes for all account-related documents.

    Attributes:
        name (String): The name of the document (required).
        doc_type (String): The type of the document (required).
    """
    name = Column(String(40), nullable=False)
    doc_type = Column(String(40), nullable=False)


class CorporateDocs(AccountDocuments, Base):
    """
    Represents corporate account-related documents.

    Attributes:
        account_no (String): Foreign key linking the document to a corporate account.
    """
    __tablename__ = "corporate_documents"
    account_no = Column(String(50), ForeignKey('corporate_accounts.account_no'))


class PersonalDocs(AccountDocuments, Base):
    """
    Represents personal account-related documents.

    Attributes:
        account_no (String): Foreign key linking the document to a personal account.
    """
    __tablename__ = "personal_documents"
    account_no = Column(String(50), ForeignKey('personal_accounts.account_no'))


class F_C_A_Docs(AccountDocuments, Base):
    """
    Represents foreign currency account-related documents.

    Attributes:
        account_no (String): Foreign key linking the document to a foreign currency account.
    """
    __tablename__ = "fca_documents"
    account_no = Column(String(50), ForeignKey('foreign_currency_accounts.account_no'))


class LoanDocs(AccountDocuments, Base):
    """
    Represents loan-related documents.

    Attributes:
        account_no (String): Foreign key linking the document to a loan account.
    """
    __tablename__ = "loan_documents"
    account_no = Column(String(50), ForeignKey('business_loans.account_no'))


class MortgageDocs(AccountDocuments, Base):
    """
    Represents mortgage-related documents.

    Attributes:
        account_no (String): Foreign key linking the document to a mortgage account.
    """
    __tablename__ = "mortgage_documents"
    account_no = Column(String(50), ForeignKey('mortgages.account_no'))

