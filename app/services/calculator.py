import math

class SavingsEngine:
    @staticmethod
    def calculate_step1_remanent(amount: float) -> float:
        """Step 1: Calculate ceiling (next multiple of 100) and remanent."""
        if amount % 100 == 0:
            return 0.0
        ceiling = math.ceil(amount / 100) * 100
        return ceiling - amount

    @staticmethod
    def calculate_investment_return(principal: float, rate: float, current_age: int, inflation: float) -> dict:
        """
        Step 5: Calculate returns using Compound Interest and dynamic Inflation Adjustment.
       
        """
        # Constraints: Retirement at 60
        t = max(60 - current_age, 0)
        
        # 1. Compound Interest: A = P(1 + r)^t
        final_amount = principal * ((1 + rate) ** t)
        
        # 2. Inflation Adjustment: Real Value = A / (1 + inflation/100)^t
        # Using the dynamic inflation value from the request
        inflation_decimal = inflation / 100
        real_return = final_amount / ((1 + inflation_decimal) ** t)
        
        return {
            "final_amount": round(final_amount, 2),
            "real_return": round(real_return, 2),
            "years_invested": t
        }

    @staticmethod
    def calculate_tax(income: float) -> float:
        """Calculates tax based on simplified slabs."""
        taxable_income = max(0, income - 50000)
        
        if taxable_income <= 700000:
            return 0
        elif taxable_income <= 1000000:
            return (taxable_income - 700000) * 0.10
        elif taxable_income <= 1200000:
            return 30000 + (taxable_income - 1000000) * 0.15
        elif taxable_income <= 1500000:
            return 60000 + (taxable_income - 1200000) * 0.20
        else:
            return 120000 + (taxable_income - 1500000) * 0.30

    @staticmethod
    def get_nps_tax_benefit(invested: float, income: float) -> float:
        """Formula: Tax(income) - Tax(income - NPS_Deduction)."""
        deduction = min(invested, 0.10 * income, 200000)
        
        current_tax = SavingsEngine.calculate_tax(income)
        new_tax = SavingsEngine.calculate_tax(income - deduction)
        
        return round(current_tax - new_tax, 2)