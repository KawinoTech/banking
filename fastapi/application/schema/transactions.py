from pydantic import BaseModel


class Transaction(BaseModel):
    """
    Represents the base structure for a transaction request.

    Attributes:
        payload (dict): A dictionary containing transaction details.
        signature (str): A string representing the transaction's signature for verification.
    """
    payload: dict
    signature: str


class Transfer(Transaction):
    """
    Represents a fund transfer transaction.

    Inherits attributes from the `Transaction` base class and adds fields specific to fund transfers.

    Attributes:
        beneficiary (str): The recipient of the transferred funds.
    """
    beneficiary: str


class PayBill(Transaction):
    """
    Represents a bill payment transaction.

    Inherits attributes from the `Transaction` base class and adds fields specific to bill payments.

    Attributes:
        account_no (str): The account number used to make the payment.
        bus_no (str): A unique identifier for the bill or utility service being paid.
    """
    account_no: str
    bus_no: str


class BuyGoods(Transaction):
    """
    Represents a transaction for buying goods.

    Inherits attributes from the `Transaction` base class and adds fields specific to purchasing goods.

    Attributes:
        store_no (str): The identifier for the store or vendor where the purchase is made.
    """
    store_no: str


class ResponseTransact(BaseModel):
    """
    Represents the response structure for a completed transaction.

    Attributes:
        ref_no (str): A unique reference number for the transaction.
    """
    ref_no: str
