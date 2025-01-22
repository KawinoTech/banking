from .models.loans import PersonalLoans, BusinessLoans, Mortgages
from datetime import datetime
from .database import session


def calculate_interest_for_loans(db=session()):
    # Fetch loans due for interest calculation
    now = datetime.now()
    due_personal_loans = db.query(PersonalLoans).all()
    due_business_loans = db.query(BusinessLoans).all()
    due_mortgage_loans = db.query(Mortgages).all()
    due_loans = [due_business_loans, due_mortgage_loans, due_personal_loans]

    for loans in due_loans:
            for loan in loans:
                n = 365
                time_elapsed = 1
                new_interest = (loan.amount * (1 + loan.rate / n)**(n * time_elapsed) - loan.amount)/10**7
                loan.outstanding_amount += new_interest
                loan.accrued_interest += new_interest
                loan.last_calculation_date = now
                db.commit()

        