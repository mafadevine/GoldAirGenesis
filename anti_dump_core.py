def is_birthright_wallet(fingerprint):
    """Checks if the wallet is a Genesis Birthright wallet."""
    return fingerprint.startswith("BIRTH-")

def try_exchange_sell(amount_gfr, fingerprint, founder_pubkey=None, is_earned=False):
    """
    Calculates how much GFR can actually be sold on the exchange.
    Enforces the 'Food Stamp' protection rule.
    """
    
    # CONSTANTS
    DUMP_THRESHOLD = 500      # The safe amount you can sell without penalty
    PENALTY_RATE = 0.90       # 90% Tax if you try to dump your birthright

    # 1. EXEMPTIONS (Freedom for Earned or Founder Assets)
    # If it's the Founder or 'Earned' money (Yield), no penalty.
    if (founder_pubkey and fingerprint == founder_pubkey) or is_earned:
        return {
            "status": "APPROVED",
            "sellable_amount": amount_gfr,
            "recycled_amount": 0,
            "message": "Standard Liquidity Transaction"
        }

    # 2. BIRTHRIGHT PROTECTION (The Iron Dome)
    if is_birthright_wallet(fingerprint):
        
        # SCENARIO A: Selling a small amount (Survival Mode)
        if amount_gfr <= DUMP_THRESHOLD:
            return {
                "status": "APPROVED",
                "sellable_amount": amount_gfr,
                "recycled_amount": 0,
                "message": "Small liquidation authorized."
            }

        # SCENARIO B: The Dump Attempt (Casino Mode)
        else:
            # Calculate the excess they are trying to dump
            excess_amount = amount_gfr - DUMP_THRESHOLD
            
            # Apply the 90% Penalty (Recycled to Community)
            recycled = int(excess_amount * PENALTY_RATE)
            
            # The amount they are allowed to keep/sell
            survivor_amount = DUMP_THRESHOLD + int(excess_amount * (1.0 - PENALTY_RATE))
            
            return {
                "status": "PENALTY_APPLIED",
                "sellable_amount": survivor_amount,
                "recycled_amount": recycled,
                "message": f"ANTI-DUMP TRIGGERED. {recycled} GFR returned to Community Pool. You cannot gamble your inheritance."
            }

    # Default Fallback
    return {"status": "ERROR", "sellable_amount": 0, "recycled_amount": 0}
