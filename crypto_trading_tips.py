# crypto_trading_tips.py

from datetime import datetime

# ──────────────────────────────────────────
# 1. Trading Tips by Category
# ──────────────────────────────────────────
TRADING_TIPS = {
    "Risk Management": [
        "Never invest more than you can afford to lose.",
        "Use the 1% rule — never risk more than 1% of your portfolio on a single trade.",
        "Always set a stop-loss before entering a trade.",
        "Diversify across multiple assets, don't put all funds in one coin.",
        "Avoid over-leveraging — high leverage can wipe your account fast."
    ],
    "Market Analysis": [
        "Always do your own research (DYOR) before buying any coin.",
        "Use both technical analysis (TA) and fundamental analysis (FA).",
        "Watch Bitcoin dominance — it often signals altcoin market trends.",
        "Monitor trading volume to confirm price movements.",
        "Use higher timeframes (4H, 1D) for stronger trade signals."
    ],
    "Trading Psychology": [
        "Never trade based on FOMO (Fear Of Missing Out).",
        "Don't let emotions drive your decisions — stick to your strategy.",
        "Accept losses as part of trading — no trader wins 100% of the time.",
        "Take breaks after a series of losses to reset your mindset.",
        "Keep a trading journal to track and learn from every trade."
    ],
    "Entry & Exit Strategy": [
        "Buy in phases (DCA) rather than investing all at once.",
        "Take partial profits at key resistance levels.",
        "Never move your stop-loss further from your entry to avoid a loss.",
        "Wait for confirmation before entering a breakout trade.",
        "Have a clear profit target before entering any trade."
    ],
    "Security While Trading": [
        "Use a dedicated device for trading — avoid personal browsing on it.",
        "Always withdraw large profits to a cold wallet.",
        "Enable withdrawal whitelist on exchanges to prevent unauthorized transfers.",
        "Never share your API keys — use read-only keys where possible.",
        "Regularly review and revoke unused exchange API permissions."
    ]
}


# ──────────────────────────────────────────
# 2. Display Tips by Category
# ──────────────────────────────────────────
def display_tips_by_category(category: str) -> None:
    """Display trading tips for a specific category."""
    if category not in TRADING_TIPS:
        print(f"  ❌ Category '{category}' not found.")
        print(f"  Available: {', '.join(TRADING_TIPS.keys())}")
        return

    print(f"\n  📂 {category}")
    print("  " + "-" * 40)
    for i, tip in enumerate(TRADING_TIPS[category], 1):
        print(f"  {i}. {tip}")


# ──────────────────────────────────────────
# 3. Display All Tips
# ──────────────────────────────────────────
def display_all_tips() -> None:
    """Display all trading tips across all categories."""
    for category in TRADING_TIPS:
        display_tips_by_category(category)
        print()


# ──────────────────────────────────────────
# 4. Daily Tip Generator
# ──────────────────────────────────────────
def get_daily_tip() -> str:
    """Returns a daily tip based on the current day of the year."""
    all_tips = [tip for tips in TRADING_TIPS.values() for tip in tips]
    day_of_year = datetime.now().timetuple().tm_yday
    tip_index = day_of_year % len(all_tips)
    return all_tips[tip_index]


# ──────────────────────────────────────────
# 5. Trading Checklist
# ──────────────────────────────────────────
def pre_trade_checklist() -> None:
    """Prints a checklist to review before entering any trade."""
    checklist = [
        "Have I analyzed the chart on a higher timeframe?",
        "Is there a clear entry point with confirmation?",
        "Have I set my stop-loss level?",
        "Have I defined my take-profit target?",
        "Am I risking more than 1% of my portfolio?",
        "Is this trade based on strategy or emotion?",
        "Have I checked the latest market news?",
        "Is my exchange account secured with 2FA?"
    ]

    print("\n  📋 PRE-TRADE CHECKLIST")
    print("  " + "-" * 40)
    for i, item in enumerate(checklist, 1):
        print(f"  ☐ {i}. {item}")
    print()


# ──────────────────────────────────────────
# 6. Risk/Reward Calculator
# ──────────────────────────────────────────
def calculate_risk_reward(entry: float, stop_loss: float, take_profit: float) -> dict:
    """Calculates the risk/reward ratio of a trade."""
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    ratio = round(reward / risk, 2) if risk > 0 else 0

    return {
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk": round(risk, 4),
        "reward": round(reward, 4),
        "risk_reward_ratio": f"1:{ratio}",
        "recommended": ratio >= 2
    }


# ──────────────────────────────────────────
# 7. Main Runner
# ──────────────────────────────────────────
def main():
    print("\n" + "="*50)
    print("   📈 Crypto Trading Tips & Tools")
    print("="*50)

    # Daily Tip
    print("\n💡 TODAY'S TRADING TIP:")
    print(f"  → {get_daily_tip()}")

    # Display tips by one category
    print("\n📌 TIPS PREVIEW — Risk Management:")
    display_tips_by_category("Risk Management")

    # Pre-trade checklist
    pre_trade_checklist()

    # Risk/Reward Calculator
    print("📌 RISK/REWARD CALCULATOR EXAMPLE")
    print("  " + "-" * 40)
    example = calculate_risk_reward(
        entry=45000,
        stop_loss=43000,
        take_profit=51000
    )
    print(f"  Entry Price    : ${example['entry']:,}")
    print(f"  Stop Loss      : ${example['stop_loss']:,}")
    print(f"  Take Profit    : ${example['take_profit']:,}")
    print(f"  Risk           : ${example['risk']:,}")
    print(f"  Reward         : ${example['reward']:,}")
    print(f"  R/R Ratio      : {example['risk_reward_ratio']}")
    print(f"  Recommended    : {'✅ Yes' if example['recommended'] else '❌ No — adjust your targets'}")

    print("\n" + "="*50)
    print("  ✅ Trading Tips Session Complete!")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
```

---

**Step-by-Step Commit Guide on Mobile:**

**Step 1 —** Go to your `crypto-safety` repo on [github.com](https://github.com).

**Step 2 —** Tap **Add file → Create new file**.

**Step 3 —** Name the file `crypto_trading_tips.py`

**Step 4 —** Paste the full code into the content area.

**Step 5 —** Write your commit message:
```
Add crypto trading tips module with risk management, psychology tips, pre-trade checklist, and risk/reward calculator
