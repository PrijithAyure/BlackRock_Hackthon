from datetime import datetime
from typing import List, Dict

class TransactionTransformer:
    @staticmethod
    def apply_rules(expenses: List[Dict], q_rules: List[Dict], p_rules: List[Dict]) -> List[Dict]:
        """Applies Step 2 (q) and Step 3 (p) logic to raw remanents."""
        processed = []
        for exp in expenses:
            date_obj = datetime.strptime(exp['date'], "%Y-%m-%d %H:%M:%S")
            remanent = exp['remanent']
            
            # Apply q-rules: Override remanent if date matches
            for q in q_rules:
                if q['start'] <= date_obj <= q['end']:
                    remanent = q['fixed']
            
            # Apply p-rules: Add extra amount if date matches
            for p in p_rules:
                if p['start'] <= date_obj <= p['end']:
                    remanent += p['extra']
            
            processed.append({**exp, "final_remanent": remanent})
        return processed

    @staticmethod
    def group_by_k(processed_expenses: List[Dict], k_periods: List[Dict]) -> List[Dict]:
        """Calculates total invested for each specified k date range."""
        results = []
        for k in k_periods:
            total = sum(
                e['final_remanent'] for e in processed_expenses 
                if k['start'] <= datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S") <= k['end']
            )
            results.append({"period": f"{k['start']} to {k['end']}", "amount_to_invest": total})
        return results