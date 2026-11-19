from banking_system import BankingSystem
 

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        # Store account_id strings and corresponding balance integers in an accounts dictionary
        self.accounts: dict[str, int] = {}

        # Store account_id strings and corresponding spending integers in an account_spending dictionary
        self.account_spending: dict[str, int] = {}

        # Start a counter tracking successful payments in order to create strings with unique payment identifiers
        self.number_of_payments: int = 0

        # Store payment information for each unique payment string
        self.payment_information: dict[str, dict] = {}

    def _process_cashback_payments(self, timestamp: int) -> None:
        """
        A helper method to refund the cashback amount for a withdrawal to an account.
        Called at the beginning of all other methods.
        Cashbacks can be processed before any other transactions are performed.
        """

        # Loop through all the payments in the dictionary to see if a cashback needs to be paid
        for payment in self.payment_information.values():

            # Process payments that have not received their cashback yet (currently in-progress)
            if payment["status"] == "IN_PROGRESS" and payment["cashback_timestamp"] <= timestamp:

                # Refund the cashback to the account
                self.accounts[payment["account_id"]] += payment["cashback"]

                # Update the status to show that the cashback was received by the account (it will not be refunded again)
                payment["status"] = "CASHBACK_RECEIVED"

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given identifier if it doesn't already exist. 
        Returns True if the account was successfully created 
        or False if an account with account_id already exists.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)

        # Return False if the account already exists
        if account_id in self.accounts:
            return False
        
        # Otherwise create it with a starting balance of 0
        else:
            self.accounts[account_id] = 0

            # add default spending of 0
            self.account_spending[account_id] = 0

            return True


    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Should transfer the given amount of money from account
        `source_account_id` to account `target_account_id`.
        Returns the balance of `source_account_id` if the transfer
        was successful or `None` otherwise.
          * Returns `None` if `source_account_id` or
          `target_account_id` doesn't exist.
          * Returns `None` if `source_account_id` and
          `target_account_id` are the same.
          * Returns `None` if account `source_account_id` has
          insufficient funds to perform the transfer.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)

        # Return None if source_account_id or target_account_id is not in the accounts dictionary
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        
        # Return None if source_account_id and target_account_id are the same
        if source_account_id == target_account_id:
            return None

        # Return None if the source account's balance is less than the desired transfer amount
        if self.accounts[source_account_id] < amount:
            return None

        # Return None if amount is negative
        if amount < 0:
            return None

        # Deduct the given amount from the source account
        self.accounts[source_account_id] -= amount

        # Add the given amount to the target account
        self.accounts[target_account_id] += amount

        # Add the transferred amount to the source account's spending
        self.account_spending[source_account_id] += amount
        
        # Return the source account's balance after transferring the given amount
        return self.accounts[source_account_id]


    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        account `account_id`.
        Returns the balance of the account after the operation has
        been processed.
        If the specified account doesn't exist, should return
        `None`.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)

        # Return None if the account to deposit into is not in the accounts dictionary 
        if account_id not in self.accounts:
            return None

        # Return None if amount is negative
        if amount < 0:
            return None

        # Add the deposited money to the account
        self.accounts[account_id] += amount

        # Return the new balance of the account
        return self.accounts[account_id]


    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest outgoing transactions - the total amount of
        money either transferred out of or paid/withdrawn (the
        **pay** operation will be introduced in level 3) - sorted in
        descending order, or in case of a tie, sorted alphabetically
        by `account_id` in ascending order.
        The result should be a list of strings in the following
        format: `["<account_id_1>(<total_outgoing_1>)", "<account_id
        _2>(<total_outgoing_2>)", ..., "<account_id_n>(<total_outgoi
        ng_n>)"]`.
            * If less than `n` accounts exist in the system, then return
            all their identifiers (in the described format).
            * Cashback (an operation that will be introduced in level 3)
            should not be reflected in the calculations for total
            outgoing transactions.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)
        
        # if n is less than or equal 0 return an empty list 
        if n <= 0:
            return []
        
        # use sorted function key, value pairs of our spending dictionary
        # set sort to sort by dict values in DESCENDING order using lambda function that returns negative value of a dict entry tuple (index 1)
        # include the account ID as a secondary sort key in ascending order to meet the following spec: 
            # in case of a tie, sorted alphabetically by `account_id` in ascending order.
        
        spending_sorted = sorted(self.account_spending.items(), 
                                    key = lambda account_value_tuple : (-account_value_tuple[1], account_value_tuple[0]))

        # now build list that is of size n from this sorted list. 
        results = []
        # if fewer than n accounts exists, slicing should still return all accounts
        for account_id, spending in spending_sorted[:n]:
            results.append(f"{account_id}({spending})")

        return results


    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        """
        Should withdraw the given amount of money from the specified
        account.
        All withdraw transactions provide a 2% cashback - 2% of the
        withdrawn amount (rounded down to the nearest integer) will
        be refunded to the account 24 hours after the withdrawal.
        If the withdrawal is successful (i.e., the account holds
        sufficient funds to withdraw the given amount), returns a
        string with a unique identifier for the payment transaction
        in this format:
        `"payment[ordinal number of withdraws from all accounts]"` -
        e.g., `"payment1"`, `"payment2"`, etc.
        Additional conditions:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if `account_id` has insufficient funds to
          perform the payment.
          * **top_spenders** should now also account for the total
          amount of money withdrawn from accounts.
          * The waiting period for cashback is 24 hours, equal to
          `24 * 60 * 60 * 1000 = 86400000` milliseconds (the unit for
          timestamps).
          So, cashback will be processed at timestamp
          `timestamp + 86400000`.
          * When it's time to process cashback for a withdrawal, the
          amount must be refunded to the account before any other
          transactions are performed at the relevant timestamp.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)

        # Return None if the account is not in the accounts dictionary 
        if account_id not in self.accounts:
            return None

        # Return None if the account has insufficient funds
        if self.accounts[account_id] < amount:
            return None

        # Return None if amount is negative
        if amount < 0:
            return None

        # Withdraw the desired amount from the account
        self.accounts[account_id] -= amount

        # Add the withdrawal amount to the account's total spending
        self.account_spending[account_id] += amount

        # Increment the successful payment counter by 1 in order to create a unique identifier string
        self.number_of_payments += 1

        # Create the unique identifier string for a payment with the specified format
        payment_string = f"payment{self.number_of_payments}"

        # Calculate a 2% cashback rounded down using integer division
        cashback = amount * 2 // 100

        # Store the payment information for the withdrawal in the payment_information dictionary (initially in progress)
        self.payment_information[payment_string] = {
            "account_id": account_id,
            "cashback": cashback, 
            "cashback_timestamp": timestamp + 86400000,
            "status": "IN_PROGRESS"
        }

        # Return the unique string for the payment if it was successful
        return payment_string

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        """
        Should return the status of the payment transaction for the
        given `payment`.
        Specifically:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if the given `payment` doesn't exist for
          the specified account.
          * Returns `None` if the payment transaction was for an
          account with a different identifier from `account_id`.
          * Returns a string representing the payment status:
          `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.
        """

        # Process the cashback for a withdrawal before any other transactions are performed at the timestamp
        self._process_cashback_payments(timestamp)

        # Return None if the account is not in the accounts dictionary 
        if account_id not in self.accounts:
            return None

        # Return None if the given payment doesn't exist for the specified account
        if payment not in self.payment_information:
            return None

        # Return None if the payment transaction was for an account with a different identifier from account_id
        if self.payment_information[payment]["account_id"] != account_id:
            return None

        # Return the status of the payment transaction for the given payment
        return self.payment_information[payment]["status"]