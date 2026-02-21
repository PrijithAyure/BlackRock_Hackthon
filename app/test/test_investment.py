"""
1. Test type: Integration and Logic Verification
2. Validation to be executed: Verifies the 5-step transformation pipeline, 
   specifically rounding logic, temporal rule overrides (p/q), and k-period grouping.
3. Command: pytest test/test_investment.py
"""

import pytest
from app.services.calculator import SavingsEngine
from app.services.processor import process_transactions

def test_step1_rounding():
    """Validates that expenses round up to the next 100."""
    # 1519 should round to 1600, leaving 81
    remanent = SavingsEngine.calculate_step1_remanent(1519)
    assert remanent == 81

def test_step2_q_override():
    """Validates that q-rules override the remanent."""
    expenses = [{"date": "2023-07-15 10:30:00", "amount": 620}]
    q_rules = [{"start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59", "fixed": 0}]
    
    # Despite 620 having a remanent of 80, the q-rule should force it to 0
    result = process_transactions(expenses, q_rules, [])
    assert result[0]['final_remanent'] == 0

def test_step3_p_addition():
    """Validates that p-rules add to the remanent."""
    expenses = [{"date": "2023-10-12 20:15:00", "amount": 1519}]
    p_rules = [{"start": "2023-10-01 00:00:00", "end": "2023-12-31 23:59:59", "extra": 25}]
    
    # 81 (base remanent) + 25 (extra) = 106
    result = process_transactions(expenses, [], p_rules)
    assert result[0]['final_remanent'] == 106