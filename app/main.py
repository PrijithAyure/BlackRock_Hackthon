from fastapi import FastAPI, HTTPException
import uvicorn
from app.schemas.investment import (
    InvestmentRequest, ParseRequest, ValidatorRequest
)
from app.services.processor import TransactionBuilder, TransactionTransformer
from app.services.validator import DataValidator
from app.services.calculator import SavingsEngine
from app.services.metrics import PerformanceMonitor

app = FastAPI(title="BlackRock Micro-Investment Challenge API")

# --- INTERNAL HELPER LOGIC ---

def _execute_investment_pipeline(data: InvestmentRequest, rate: float, is_nps: bool):
    """
    Unified pipeline for Steps 1-5 of the BlackRock Challenge.
   
    """
    # 1. Enrich: Calculate ceiling/remanent
    enriched = TransactionBuilder.parse_expenses([t.model_dump() for t in data.transactions])
    
    # 2 & 3. Transform: Apply q-overrides and p-additions
    processed = TransactionTransformer.apply_rules(
        enriched, 
        [q.model_dump() for q in data.q], 
        [p.model_dump() for p in data.p]
    )
    
    savings_by_dates = []
    total_tx_amount = sum(t.amount for t in data.transactions)
    total_ceiling = sum(e['ceiling'] for e in enriched)

    # 4. Group: Aggregate by k-periods
    for k_period in data.k:
        k_data = k_period.model_dump()
        period_sum = sum(
            item['final_remanent'] for item in processed 
            if k_data['start'] <= item['date'] <= k_data['end']
        )
        
        # 5. Project: Compound Interest & Inflation
        results = SavingsEngine.calculate_investment_return(
            period_sum, rate=rate, current_age=data.age, inflation=data.inflation
        )
        
        # Tax logic: NPS only
        tax_benefit = 0.0
        if is_nps:
            tax_benefit = SavingsEngine.get_nps_tax_benefit(period_sum, data.wage * 12)

        savings_by_dates.append({
            "start": k_data['start'],
            "end": k_data['end'],
            "amount": round(float(period_sum), 2),
            "profit": round(float(results['real_return'] - period_sum), 2),
            "taxBenefit": round(float(tax_benefit), 2)
        })

    return {
        "totalTransactionAmount": total_tx_amount,
        "totalCeiling": total_ceiling,
        "savingsByDates": savings_by_dates
    }

# --- PUBLIC ENDPOINTS ---

@app.post("/blackrock/challenge/v1/transactions:parse")
async def parse_transactions(data: ParseRequest):
    """Target: Step 1 - Enrichment"""
    return TransactionBuilder.parse_expenses([e.model_dump() for e in data.expenses])

@app.post("/blackrock/challenge/v1/transactions:validator")
async def validate_transactions(data: ValidatorRequest):
    """Target: Step 2 - Data Integrity"""
    return DataValidator.validate_transactions(data.wage, [t.model_dump() for t in data.transactions])

@app.post("/blackrock/challenge/v1/returns:nps")
async def calculate_nps_returns(data: InvestmentRequest):
    """Target: Final Calculation (NPS @ 7.11%)"""
    try:
        return _execute_investment_pipeline(data, rate=0.0711, is_nps=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/blackrock/challenge/v1/returns:index")
async def calculate_index_returns(data: InvestmentRequest):
    """Target: Final Calculation (Index Fund @ 14.49%)"""
    try:
        return _execute_investment_pipeline(data, rate=0.1449, is_nps=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/blackrock/challenge/v1/performance")
def get_performance():
    """Reports system execution metrics: time, memory, and threads."""
    return PerformanceMonitor.get_system_metrics()
if __name__ == "__main__":
    # Explicitly binding to 0.0.0.0 allows the container to talk to the host
    uvicorn.run(app, host="0.0.0.0", port=5477)