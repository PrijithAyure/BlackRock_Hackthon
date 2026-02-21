import math
from datetime import datetime
from typing import List, Dict
from app.services.calculator import SavingsEngine

class TransactionBuilder:
    @staticmethod
    def parse_expenses(expenses: List[Dict]) -> List[Dict]:
        """
        Step 1: Enriches raw expenses with ceiling and remanent.
        Target: /transactions:parse
        """
        enriched = []
        for exp in expenses:
            # Ceiling is the next multiple of 100
            ceiling = math.ceil(exp['amount'] / 100) * 100
            remanent = ceiling - exp['amount']
            
            enriched.append({
                "date": exp['date'],
                "amount": exp['amount'],
                "ceiling": ceiling,
                "remanent": remanent
            })
        return enriched

class TransactionTransformer:
    @staticmethod
    def apply_rules(enriched_txs: List[Dict], q_rules: List[Dict], p_rules: List[Dict]) -> List[Dict]:
        """
        Step 2 & 3: Implements q-overrides and p-additions logic.
        Target: /returns calculation pipeline
        """
        processed_results = []

        for tx in enriched_txs:
            remanent = tx['remanent']
            exp_date = datetime.strptime(tx['date'], "%Y-%m-%d %H:%M:%S")

            # Step 2: Apply q period rules (Fixed Amount Override)
            # Logic: If multiple match, use the one that starts latest
            matching_q = [
                q for q in q_rules 
                if datetime.strptime(q['start'], "%Y-%m-%d %H:%M:%S") <= exp_date <= datetime.strptime(q['end'], "%Y-%m-%d %H:%M:%S")
            ]
            if matching_q:
                latest_q = sorted(matching_q, key=lambda x: x['start'], reverse=True)[0]
                remanent = latest_q['fixed']

            # Step 3: Apply p period rules (Extra Amount Addition)
            # Logic: Add all matching extra amounts together
            for p in p_rules:
                p_start = datetime.strptime(p['start'], "%Y-%m-%d %H:%M:%S")
                p_end = datetime.strptime(p['end'], "%Y-%m-%d %H:%M:%S")
                if p_start <= exp_date <= p_end:
                    remanent += p['extra']

            processed_results.append({
                **tx,
                "final_remanent": remanent
            })

        return processed_results