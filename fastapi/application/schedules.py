from .models.loans import PersonalLoans, BusinessLoans, Mortgages
from .models.term_deposits import TermDeposit
from datetime import datetime
from .database import session


def calculate_interest_for_loans(db=session()):
    """
    Calculates and updates interest for all types of loans (Personal, Business, Mortgages).
    
    - Fetches all the loans from the database.
    - Calculates the interest for each loan based on the formula.
    - Updates the outstanding amount and accrued interest for each loan.
    - Commits the changes to the database.
    """
    # Fetch loans due for interest calculation
    now = datetime.now()
    due_personal_loans = db.query(PersonalLoans).all()
    due_business_loans = db.query(BusinessLoans).all()
    due_mortgage_loans = db.query(Mortgages).all()
    due_loans = [due_business_loans, due_mortgage_loans, due_personal_loans]

    for loans in due_loans:
        for loan in loans:
            n = 365  # Number of days in a year (for daily compounding)
            time_elapsed = 1  # Time elapsed in years (set to 1 for annual calculation)
            
            # Compound Interest Calculation: A = P * (1 + r/n)^(nt) - P
            new_interest = (loan.amount * (1 + loan.rate / n)**(n * time_elapsed) - loan.amount) / 10**7  # Adjusting the scale for correct units
            
            loan.outstanding_amount += new_interest
            loan.accrued_interest += new_interest
            loan.last_calculation_date = now
            db.commit()

def calculate_interest_for_tds(db=session()):
    """
    Calculates and updates interest for all active term deposits.

    - Fetches all the term deposits from the database.
    - Calculates the interest for each term deposit based on the formula.
    - Updates the accumulated value and interest for each term deposit.
    - Commits the changes to the database.
    """
    # Fetch term deposits due for interest calculation
    due_term_deposits = db.query(TermDeposit).all()

    for td in due_term_deposits:
        n = 365  # Number of days in a year (for daily compounding)
        time_elapsed = 1  # Time elapsed in years (set to 1 for annual calculation)
        
        # Compound Interest Calculation: A = P * (1 + r/n)^(nt) - P
        new_interest = (td.amount * (1 + td.rate / n)**(n * time_elapsed) - td.amount) / 10**4  # Adjusting scale for correct units
        
        td.interest += new_interest
        td.accumulated_value += new_interest
        db.commit()
