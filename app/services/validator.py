from typing import List, Dict

class DataValidator:
    @staticmethod
    def validate_transactions(wage: float, transactions: List[Dict]) -> Dict:
        """
        Filters transactions into valid and invalid lists.
       
        """
        valid = []
        invalid = []
        
        for tx in transactions:
            # Rule 1: Negative amounts are strictly prohibited
            if tx['amount'] < 0:
                invalid_tx = tx.copy()
                invalid_tx["message"] = "Negative amounts are not allowed"
                invalid.append(invalid_tx)
            
            # Additional Rule (Optional): Transactions exceeding the monthly wage
            # Based on the challenge context, you could add logic to flag 
            # transactions that appear unrealistic relative to the user's income.
            else:
                valid.append(tx)
        
        return {
            "valid": valid,
            "invalid": invalid
        }