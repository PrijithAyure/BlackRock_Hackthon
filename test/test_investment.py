"""
1. Test type: Integration and Logic Verification
2. Validation to be executed: Verifies the 5-step transformation pipeline, 
   specifically rounding logic, temporal rule overrides (p/q), and k-period grouping.
3. Command: pytest test/test_investment.py
"""

import pytest
from app.services.calculator import SavingsEngine
from app.services.processor import TransactionBuilder, TransactionTransformer

def test_step1_rounding():
    """Validates that expenses round up to the next 100."""
    # 1519 should round to 1600, leaving 81
    remanent = SavingsEngine.calculate_step1_remanent(1519)
    assert remanent == 81

def test_step2_q_override():
    """Validates that q-rules override the remanent."""
    # Use TransactionBuilder to create the initial enriched transaction
    expenses = [{"date": "2023-07-15 10:30:00", "amount": 620}]
    enriched = TransactionBuilder.parse_expenses(expenses)
    
    # Apply q-rules: 620 rounds to 700 (remanent 80), but q-rule forces it to 0
    q_rules = [{"start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59", "fixed": 0}]
    result = TransactionTransformer.apply_rules(enriched, q_rules, [])
    assert result[0]['final_remanent'] == 0

def test_step3_p_addition():
    """Validates that p-rules add to the remanent."""
    expenses = [{"date": "2023-10-12 20:15:00", "amount": 1519}]
    enriched = TransactionBuilder.parse_expenses(expenses)
    
    # 81 (base remanent) + 25 (extra) = 106
    p_rules = [{"start": "2023-10-01 00:00:00", "end": "2023-12-31 23:59:59", "extra": 25}]
    result = TransactionTransformer.apply_rules(enriched, [], p_rules)
    assert result[0]['final_remanent'] == 106