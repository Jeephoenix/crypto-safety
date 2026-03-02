# gas_fee_estimator.py
# A complete Gas Fee Estimator for Ethereum transactions
# Simulates real-world gas calculations, transaction types,
# network congestion levels, and multi-chain fee comparisons

import time
import secrets
import json
from datetime import datetime

divider = lambda title="": print(
    f"\n  {'═' * 55}\n  {title}\n  {'═' * 55}" if title
    else f"\n  {'─' * 55}"
)


# ══════════════════════════════════════════════════════════
# 1. WHAT IS GAS — Concept Explainer
# ══════════════════════════════════════════════════════════
GAS_CONCEPTS = {
    "Gas": (
        "Gas is the unit that measures the computational effort "
        "required to execute a transaction or smart contract on "
        "Ethereum. Think of it like fuel for a car — every "
        "operation on the blockchain costs a certain amount of gas."
    ),
    "Gas Price": (
        "Gas price is how much ETH you are willing to pay per unit "
        "of gas. It is measured in Gwei (1 Gwei = 0.000000001 ETH). "
        "Higher gas price = faster transaction confirmation."
    ),
    "Gas Limit": (
        "Gas limit is the maximum amount of gas you allow a "
        "transaction to consume. For a simple ETH transfer it is "
        "always 21,000. For smart contracts it can be much higher."
    ),
    "Base Fee": (
        "Introduced in EIP-1559, the base fee is the minimum gas "
        "price required for a transaction to be included in a block. "
        "It is burned (destroyed) instead of paid to miners."
    ),
    "Priority Fee": (
        "Also called a tip. This goes directly to the validator "
        "as an incentive to include your transaction faster. "
        "Higher tip = higher priority in the mempool."
    ),
    "Max Fee": (
        "The maximum total amount per gas you are willing to pay. "
        "Formula: Max Fee = Base Fee + Priority Fee. "
        "Any unused amount above base fee is refunded to you."
    ),
    "Gwei": (
        "Gwei is the unit used to measure gas prices. "
        "1 ETH = 1,000,000,000 Gwei. "
        "Typical gas prices range from 5 Gwei (slow) to 200+ Gwei (fast)."
    ),
    "Mempool": (
        "The mempool (memory pool) is a waiting room for unconfirmed "
        "transactions. Validators pick transactions from the mempool "
        "starting with the highest tips first."
    ),
    "EIP-1559": (
        "A major Ethereum upgrade that changed how gas fees work. "
        "It introduced base fees (burned) and priority fees (tips), "
        "making gas fees more predictable and reducing ETH supply."
    ),
    "Gas War": (
        "A gas war happens when many users compete to get their "
        "transactions included quickly — like during a popular NFT "
        "mint. Everyone raises their gas price, causing fees to spike."
    )
}


# ══════════════════════════════════════════════════════════
# 2. TRANSACTION TYPES & BASE GAS COSTS
# ══════════════════════════════════════════════════════════
TRANSACTION_TYPES = {
    "ETH Transfer": {
        "gas_limit": 21_000,
        "description": "Simple send ETH from one wallet to another",
        "complexity": "Low"
    },
    "ERC-20 Token Transfer": {
        "gas_limit": 65_000,
        "description": "Send an ERC-20 token (USDT, LINK, UNI etc.)",
        "complexity": "Low"
    },
    "ERC-20 Token Approval": {
        "gas_limit": 46_000,
        "description": "Approve a contract to spend your tokens",
        "complexity": "Low"
    },
    "Uniswap Token Swap": {
        "gas_limit": 150_000,
        "description": "Swap tokens on Uniswap V3",
        "complexity": "Medium"
    },
    "NFT Transfer": {
        "gas_limit": 84_000,
        "description": "Transfer an ERC-721 NFT to another wallet",
        "complexity": "Low"
    },
    "NFT Mint": {
        "gas_limit": 185_000,
        "description": "Mint a new NFT from a collection",
        "complexity": "Medium"
    },
    "Smart Contract Deploy": {
        "gas_limit": 500_000,
        "description": "Deploy a new smart contract to the network",
        "complexity": "High"
    },
    "Liquidity Add (DeFi)": {
        "gas_limit": 230_000,
        "description": "Add liquidity to a DeFi pool",
        "complexity": "High"
    },
    "Liquidity Remove (DeFi)": {
        "gas_limit": 200_000,
        "description": "Remove liquidity from a DeFi pool",
        "complexity": "High"
    },
    "Yield Farm Stake": {
        "gas_limit": 120_000,
        "description": "Stake tokens in a yield farming contract",
        "complexity": "Medium"
    },
    "DAO Vote": {
        "gas_limit": 90_000,
        "description": "Cast a vote in a DAO governance contract",
        "complexity": "Medium"
    },
    "Multisig Transaction": {
        "gas_limit": 140_000,
        "description": "Execute a multi-signature wallet transaction",
        "complexity": "Medium"
    }
}


# ══════════════════════════════════════════════════════════
# 3. NETWORK CONGESTION SIMULATOR
# ══════════════════════════════════════════════════════════
CONGESTION_LEVELS = {
    "Very Low": {
        "base_fee_gwei": 5,
        "description": "Network is quiet. Rare — usually late night UTC.",
        "wait_time": "Under 15 seconds",
        "emoji": "🟢"
    },
    "Low": {
        "base_fee_gwei": 12,
        "description": "Light traffic. Good time to transact.",
        "wait_time": "15–30 seconds",
        "emoji": "🟢"
    },
    "Moderate": {
        "base_fee_gwei": 25,
        "description": "Normal daytime activity.",
        "wait_time": "30–60 seconds",
        "emoji": "🟡"
    },
    "High": {
        "base_fee_gwei": 60,
        "description": "Busy period. Popular DeFi or NFT activity.",
        "wait_time": "1–3 minutes",
        "emoji": "🟠"
    },
    "Very High": {
        "base_fee_gwei": 120,
        "description": "Heavy congestion. Major event or NFT mint.",
        "wait_time": "3–10 minutes",
        "emoji": "🔴"
    },
    "Extreme": {
        "base_fee_gwei": 300,
        "description": "Gas war. Network nearly unusable for small txns.",
        "wait_time": "10+ minutes or dropped",
        "emoji": "🚨"
    }
}


# ══════════════════════════════════════════════════════════
# 4. SPEED TIERS
# ══════════════════════════════════════════════════════════
SPEED_TIERS = {
    "Slow": {
        "priority_fee_gwei": 0.5,
        "multiplier": 0.9,
        "wait": "2–5 minutes",
        "description": "Cheapest option. May take a while.",
        "emoji": "🐢"
    },
    "Standard": {
        "priority_fee_gwei": 1.5,
        "multiplier": 1.0,
        "wait": "30–60 seconds",
        "description": "Balanced speed and cost.",
        "emoji": "🚗"
    },
    "Fast": {
        "priority_fee_gwei": 3.0,
        "multiplier": 1.2,
        "wait": "15–30 seconds",
        "description": "Higher priority in mempool.",
        "emoji": "🚀"
    },
    "Instant": {
        "priority_fee_gwei": 8.0,
        "multiplier": 1.5,
        "wait": "Next block (~12 seconds)",
        "description": "Maximum priority. Used in gas wars.",
        "emoji": "⚡"
    }
}


# ══════════════════════════════════════════════════════════
# 5. MULTI-CHAIN FEE COMPARISON
# ══════════════════════════════════════════════════════════
CHAINS = {
    "Ethereum Mainnet": {
        "symbol": "ETH",
        "eth_price_usd": 3200,
        "avg_base_fee_gwei": 25,
        "block_time_sec": 12,
        "finality": "~2 minutes",
        "security": "Highest",
        "decentralization": "Highest",
        "emoji": "⟠"
    },
    "Polygon (MATIC)": {
        "symbol": "MATIC",
        "eth_price_usd": 0.85,
        "avg_base_fee_gwei": 80,
        "block_time_sec": 2,
        "finality": "~4 seconds",
        "security": "High",
        "decentralization": "High",
        "emoji": "🟣"
    },
    "Arbitrum One": {
        "symbol": "ETH",
        "eth_price_usd": 3200,
        "avg_base_fee_gwei": 0.1,
        "block_time_sec": 0.25,
        "finality": "~1 second",
        "security": "High (L2)",
        "decentralization": "High",
        "emoji": "🔵"
    },
    "Optimism": {
        "symbol": "ETH",
        "eth_price_usd": 3200,
        "avg_base_fee_gwei": 0.05,
        "block_time_sec": 2,
        "finality": "~2 seconds",
        "security": "High (L2)",
        "decentralization": "High",
        "emoji": "🔴"
    },
    "Base": {
        "symbol": "ETH",
        "eth_price_usd": 3200,
        "avg_base_fee_gwei": 0.03,
        "block_time_sec": 2,
        "finality": "~2 seconds",
        "security": "High (L2)",
        "decentralization": "Medium",
        "emoji": "🔷"
    },
    "BNB Smart Chain": {
        "symbol": "BNB",
        "eth_price_usd": 380,
        "avg_base_fee_gwei": 3,
        "block_time_sec": 3,
        "finality": "~6 seconds",
        "security": "Medium",
        "decentralization": "Medium",
        "emoji": "🟡"
    },
    "Avalanche (C-Chain)": {
        "symbol": "AVAX",
        "eth_price_usd": 28,
        "avg_base_fee_gwei": 25,
        "block_time_sec": 2,
        "finality": "~2 seconds",
        "security": "High",
        "decentralization": "High",
        "emoji": "🔺"
    },
    "Sepolia Testnet": {
        "symbol": "SepoliaETH",
        "eth_price_usd": 0,
        "avg_base_fee_gwei": 10,
        "block_time_sec": 12,
        "finality": "~2 minutes",
        "security": "Testnet",
        "decentralization": "Testnet",
        "emoji": "🧪"
    }
}


# ══════════════════════════════════════════════════════════
# 6. GAS FEE CALCULATOR ENGINE
# ══════════════════════════════════════════════════════════
class GasFeeCalculator:
    """
    Core gas fee calculation engine.
    Simulates real EIP-1559 fee structure.
    """

    def __init__(self, eth_price_usd: float = 3200.0):
        self.eth_price_usd = eth_price_usd
        self.calculation_history = []

    def gwei_to_eth(self, gwei: float) -> float:
        return gwei / 1_000_000_000

    def eth_to_usd(self, eth: float) -> float:
        return eth * self.eth_price_usd

    def calculate_fee(
        self,
        transaction_type: str,
        congestion_level: str,
        speed_tier: str,
        chain: str = "Ethereum Mainnet"
    ) -> dict:
        """
        Calculate gas fee for a transaction.
        Uses EIP-1559 formula:
        Total Fee = (Base Fee + Priority Fee) × Gas Used
        """

        if transaction_type not in TRANSACTION_TYPES:
            return {"error": f"Unknown transaction type: {transaction_type}"}
        if congestion_level not in CONGESTION_LEVELS:
            return {"error": f"Unknown congestion level: {congestion_level}"}
        if speed_tier not in SPEED_TIERS:
            return {"error": f"Unknown speed tier: {speed_tier}"}
        if chain not in CHAINS:
            return {"error": f"Unknown chain: {chain}"}

        tx          = TRANSACTION_TYPES[transaction_type]
        congestion  = CONGESTION_LEVELS[congestion_level]
        speed       = SPEED_TIERS[speed_tier]
        chain_info  = CHAINS[chain]

        # Core EIP-1559 calculation
        base_fee_gwei       = congestion["base_fee_gwei"] * speed["multiplier"]
        priority_fee_gwei   = speed["priority_fee_gwei"]
        max_fee_gwei        = base_fee_gwei + priority_fee_gwei
        gas_limit           = tx["gas_limit"]

        # Total fee calculation
        total_fee_gwei  = max_fee_gwei * gas_limit
        total_fee_eth   = self.gwei_to_eth(total_fee_gwei)
        total_fee_usd   = self.eth_to_usd(total_fee_eth) * (
            chain_info["eth_price_usd"] / 3200
        )

        # Burned vs tip breakdown
        burned_gwei     = base_fee_gwei * gas_limit
        tip_gwei        = priority_fee_gwei * gas_limit
        burned_eth      = self.gwei_to_eth(burned_gwei)
        tip_eth         = self.gwei_to_eth(tip_gwei)

        result = {
            "transaction_type"  : transaction_type,
            "chain"             : chain,
            "congestion"        : congestion_level,
            "speed"             : speed_tier,
            "gas_limit"         : gas_limit,
            "base_fee_gwei"     : round(base_fee_gwei, 4),
            "priority_fee_gwei" : round(priority_fee_gwei, 4),
            "max_fee_gwei"      : round(max_fee_gwei, 4),
            "total_fee_gwei"    : round(total_fee_gwei, 2),
            "total_fee_eth"     : round(total_fee_eth, 8),
            "total_fee_usd"     : round(total_fee_usd, 4),
            "burned_eth"        : round(burned_eth, 8),
            "tip_eth"           : round(tip_eth, 8),
            "estimated_wait"    : speed["wait"],
            "block_time"        : f"{chain_info['block_time_sec']}s",
            "timestamp"         : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tx_hash_preview"   : "0x" + secrets.token_hex(8) + "..."
        }

        self.calculation_history.append(result)
        return result

    def compare_speeds(
        self,
        transaction_type: str,
        congestion_level: str,
        chain: str = "Ethereum Mainnet"
    ) -> list:
        """Compare all speed tiers for a given transaction."""
        return [
            self.calculate_fee(
                transaction_type, congestion_level, speed, chain
            )
            for speed in SPEED_TIERS.keys()
        ]

    def compare_chains(
        self,
        transaction_type: str = "ETH Transfer"
    ) -> list:
        """Compare gas fees across all supported chains."""
        results = []
        for chain_name in CHAINS.keys():
            congestion = "Moderate"
            result = self.calculate_fee(
                transaction_type, congestion, "Standard", chain_name
            )
            results.append(result)
        return results

    def estimate_daily_cost(
        self,
        transactions: list,
        congestion_level: str = "Moderate"
    ) -> dict:
        """
        Estimate total daily gas cost for a set of transactions.
        transactions = [{"type": "ETH Transfer", "count": 3}, ...]
        """
        total_eth = 0
        total_usd = 0
        breakdown = []

        for item in transactions:
            tx_type = item.get("type")
            count   = item.get("count", 1)
            result  = self.calculate_fee(
                tx_type, congestion_level, "Standard"
            )
            subtotal_eth = result["total_fee_eth"] * count
            subtotal_usd = result["total_fee_usd"] * count
            total_eth   += subtotal_eth
            total_usd   += subtotal_usd
            breakdown.append({
                "type"          : tx_type,
                "count"         : count,
                "cost_per_tx"   : f"${result['total_fee_usd']:.4f}",
                "subtotal_usd"  : f"${subtotal_usd:.4f}"
            })

        return {
            "congestion_level"  : congestion_level,
            "total_transactions": sum(i["count"] for i in transactions),
            "total_eth"         : round(total_eth, 8),
            "total_usd"         : round(total_usd, 4),
            "breakdown"         : breakdown
        }

    def get_savings_tip(self, fee_usd: float) -> str:
        """Returns a money-saving tip based on fee amount."""
        if fee_usd < 1:
            return "✅ Great time to transact — fees are very low!"
        elif fee_usd < 5:
            return "💡 Fees are reasonable. Standard speed is fine."
        elif fee_usd < 20:
            return "⚠️  Consider waiting for lower congestion or use a Layer 2."
        elif fee_usd < 50:
            return "🔴 Fees are high. Use Arbitrum or Polygon instead."
        else:
            return "🚨 Extreme fees! Wait or switch chains immediately."


# ══════════════════════════════════════════════════════════
# 7. GAS TRACKER — Network Snapshot
# ══════════════════════════════════════════════════════════
class GasTracker:
    """Simulates a real-time gas price tracker."""

    def __init__(self):
        self.snapshots = []

    def take_snapshot(self) -> dict:
        """Simulates fetching current gas prices from network."""
        import random
        base = random.uniform(8, 80)
        snapshot = {
            "timestamp"     : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "slow_gwei"     : round(base * 0.85, 1),
            "standard_gwei" : round(base, 1),
            "fast_gwei"     : round(base * 1.3, 1),
            "instant_gwei"  : round(base * 1.8, 1),
            "base_fee_gwei" : round(base * 0.9, 1),
            "network_load"  : self._get_load_label(base)
        }
        self.snapshots.append(snapshot)
        return snapshot

    def _get_load_label(self, base_fee: float) -> str:
        if base_fee < 15:   return "🟢 Very Low"
        elif base_fee < 25: return "🟢 Low"
        elif base_fee < 40: return "🟡 Moderate"
        elif base_fee < 65: return "🟠 High"
        elif base_fee < 100: return "🔴 Very High"
        else:               return "🚨 Extreme"

    def simulate_price_history(self, hours: int = 6) -> list:
        """Simulate gas price history over N hours."""
        import random
        history = []
        base = 25.0
        for i in range(hours * 4):
            base += random.uniform(-5, 5)
            base = max(5, min(150, base))
            history.append({
                "time"      : f"T-{hours}h + {i * 15}min",
                "gwei"      : round(base, 1),
                "load"      : self._get_load_label(base)
            })
        return history


# ══════════════════════════════════════════════════════════
# 8. DISPLAY FUNCTIONS
# ══════════════════════════════════════════════════════════
def display_concepts() -> None:
    divider("📚 GAS FEE CONCEPTS EXPLAINED")
    for term, explanation in GAS_CONCEPTS.items():
        print(f"\n  📖 {term}")
        print(f"  {explanation}")


def display_fee_result(result: dict) -> None:
    """Pretty print a single fee calculation result."""
    if "error" in result:
        print(f"  ❌ Error: {result['error']}")
        return

    print(f"\n  {'─' * 50}")
    print(f"  📋 Transaction  : {result['transaction_type']}")
    print(f"  🌐 Chain        : {result['chain']}")
    print(f"  📊 Congestion   : {result['congestion']}")
    print(f"  ⚡ Speed        : {result['speed']}")
    print(f"  {'─' * 50}")
    print(f"  ⛽ Gas Limit    : {result['gas_limit']:,} units")
    print(f"  📉 Base Fee     : {result['base_fee_gwei']} Gwei")
    print(f"  💸 Priority Fee : {result['priority_fee_gwei']} Gwei")
    print(f"  📈 Max Fee      : {result['max_fee_gwei']} Gwei")
    print(f"  {'─' * 50}")
    print(f"  💰 Total (Gwei) : {result['total_fee_gwei']:,} Gwei")
    print(f"  💰 Total (ETH)  : {result['total_fee_eth']} ETH")
    print(f"  💵 Total (USD)  : ${result['total_fee_usd']}")
    print(f"  {'─' * 50}")
    print(f"  🔥 Burned       : {result['burned_eth']} ETH")
    print(f"  🎁 Tip          : {result['tip_eth']} ETH")
    print(f"  ⏱️  Est. Wait    : {result['estimated_wait']}")
    print(f"  🔗 TX Preview   : {result['tx_hash_preview']}")


def display_speed_comparison(results: list) -> None:
    divider("⚡ SPEED TIER COMPARISON")
    print(f"\n  {'Speed':<12} {'Gwei':<10} {'ETH':<15} {'USD':<12} {'Wait'}")
    print(f"  {'─' * 60}")
    for r in results:
        speed   = SPEED_TIERS[r["speed"]]
        print(
            f"  {speed['emoji']} {r['speed']:<10} "
            f"{r['max_fee_gwei']:<10} "
            f"{r['total_fee_eth']:<15} "
            f"${r['total_fee_usd']:<11} "
            f"{r['estimated_wait']}"
        )


def display_chain_comparison(results: list) -> None:
    divider("🌐 MULTI-CHAIN GAS FEE COMPARISON")
    print(f"\n  {'Chain':<25} {'Symbol':<8} {'USD Cost':<12} {'Speed':<15} {'Security'}")
    print(f"  {'─' * 75}")
    for r in results:
        chain = CHAINS[r["chain"]]
        cost  = f"${r['total_fee_usd']}" if chain["eth_price_usd"] > 0 else "FREE"
        print(
            f"  {chain['emoji']} {r['chain']:<23} "
            f"{chain['symbol']:<8} "
            f"{cost:<12} "
            f"{chain['finality']:<15} "
            f"{chain['security']}"
        )


def display_daily_estimate(estimate: dict) -> None:
    divider("📅 DAILY TRANSACTION COST ESTIMATE")
    print(f"\n  Congestion Level : {estimate['congestion_level']}")
    print(f"  Total Transactions: {estimate['total_transactions']}")
    print(f"\n  {'Transaction':<30} {'Count':<8} {'Per TX':<14} {'Subtotal'}")
    print(f"  {'─' * 65}")
    for item in estimate["breakdown"]:
        print(
            f"  {item['type']:<30} "
            f"{item['count']:<8} "
            f"{item['cost_per_tx']:<14} "
            f"{item['subtotal_usd']}"
        )
    print(f"  {'─' * 65}")
    print(f"  {'TOTAL':<30} {estimate['total_transactions']:<8} {'':14} ${estimate['total_usd']}")
    print(f"  Total in ETH: {estimate['total_eth']} ETH")


def display_gas_tracker(snapshot: dict) -> None:
    divider("📡 LIVE GAS TRACKER SNAPSHOT")
    print(f"\n  🕐 Timestamp   : {snapshot['timestamp']}")
    print(f"  📊 Network Load: {snapshot['network_load']}")
    print(f"\n  🐢 Slow        : {snapshot['slow_gwei']} Gwei")
    print(f"  🚗 Standard    : {snapshot['standard_gwei']} Gwei")
    print(f"  🚀 Fast        : {snapshot['fast_gwei']} Gwei")
    print(f"  ⚡ Instant     : {snapshot['instant_gwei']} Gwei")
    print(f"  🔥 Base Fee    : {snapshot['base_fee_gwei']} Gwei")


def display_price_history(history: list) -> None:
    divider("📈 GAS PRICE HISTORY (Last 6 Hours)")
    print(f"\n  {'Time':<25} {'Gwei':<10} Load")
    print(f"  {'─' * 50}")
    step = max(1, len(history) // 12)
    for entry in history[::step]:
        bar = "█" * int(entry["gwei"] / 10)
        print(f"  {entry['time']:<25} {entry['gwei']:<10} {bar}")


def display_saving_tips() -> None:
    divider("💡 GAS SAVING TIPS")
    tips = [
        ("Transact during off-peak hours",
         "Gas fees are lowest late night or early morning UTC (00:00–08:00)."),
        ("Use Layer 2 networks",
         "Arbitrum, Optimism, and Base offer 10–100x cheaper fees than mainnet."),
        ("Batch your transactions",
         "Instead of 5 separate txns, use protocols that batch them into one."),
        ("Set custom gas limits",
         "Use Slow speed for non-urgent transactions to save significantly."),
        ("Monitor gas trackers",
         "Use etherscan.io/gastracker or blocknative.com before transacting."),
        ("Avoid gas wars",
         "Never participate in NFT mints during peak hours unless necessary."),
        ("Use gas tokens",
         "Some protocols let you pre-purchase gas when cheap and use it later."),
        ("Check EIP-1559 base fee trends",
         "If base fee is falling, wait a few blocks before sending."),
        ("Use Polygon for small transactions",
         "For transactions under $50 in value, mainnet fees may not be worth it."),
        ("Approve exact amounts",
         "Set token approvals to exact amounts instead of unlimited to save gas.")
    ]
    for i, (title, detail) in enumerate(tips, 1):
        print(f"\n  💡 Tip {i}: {title}")
        print(f"  → {detail}")


# ══════════════════════════════════════════════════════════
# 9. MAIN RUNNER
# ══════════════════════════════════════════════════════════
def main():
    print("\n" + "=" * 60)
    print("   ⛽ Ethereum Gas Fee Estimator — Complete Guide")
    print("=" * 60)

    calc    = GasFeeCalculator(eth_price_usd=3200)
    tracker = GasTracker()

    # ── Core concepts ──────────────────────────────────
    print("\n\n  📌 SPOTLIGHT CONCEPTS")
    divider()
    for term in ["Gas", "Gas Price", "Base Fee", "Priority Fee", "EIP-1559"]:
        print(f"\n  📖 {term}: {GAS_CONCEPTS[term]}")

    # ── Live gas tracker ───────────────────────────────
    snapshot = tracker.take_snapshot()
    display_gas_tracker(snapshot)

    # ── Gas price history ──────────────────────────────
    history = tracker.simulate_price_history(hours=6)
    display_price_history(history)

    # ── Single fee calculations ────────────────────────
    divider("📌 SAMPLE FEE CALCULATIONS")

    calculations = [
        ("ETH Transfer",            "Low",       "Standard"),
        ("Uniswap Token Swap",      "Moderate",  "Fast"),
        ("NFT Mint",                "High",      "Instant"),
        ("Smart Contract Deploy",   "Moderate",  "Standard"),
        ("DAO Vote",                "Low",       "Slow"),
    ]

    for tx_type, congestion, speed in calculations:
        result = calc.calculate_fee(tx_type, congestion, speed)
        display_fee_result(result)
        tip = calc.get_savings_tip(result["total_fee_usd"])
        print(f"\n  {tip}")

    # ── Speed tier comparison ──────────────────────────
    speed_results = calc.compare_speeds("Uniswap Token Swap", "High")
    display_speed_comparison(speed_results)

    # ── Multi-chain comparison ─────────────────────────
    chain_results = calc.compare_chains("ETH Transfer")
    display_chain_comparison(chain_results)

    # ── Daily cost estimator ───────────────────────────
    daily_txns = [
        {"type": "ETH Transfer",           "count": 3},
        {"type": "ERC-20 Token Transfer",  "count": 5},
        {"type": "Uniswap Token Swap",     "count": 2},
        {"type": "NFT Transfer",           "count": 1},
        {"type": "DAO Vote",               "count": 2},
    ]
    estimate = calc.estimate_daily_cost(daily_txns, "Moderate")
    display_daily_estimate(estimate)

    # ── Saving tips ────────────────────────────────────
    display_saving_tips()

    # ── Summary ────────────────────────────────────────
    print("\n\n" + "=" * 60)
    print("  ⛽ Gas Fee Estimator Complete!")
    print(f"  📊 Total Calculations Run : {len(calc.calculation_history)}")
    print(f"  🌐 Chains Covered         : {len(CHAINS)}")
    print(f"  📋 Transaction Types      : {len(TRANSACTION_TYPES)}")
    print(f"  💡 Gas Saving Tips        : 10")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
```

---

**Step-by-Step Commit Guide on Mobile:**

**Step 1 —** Go to your `crypto-safety` repo on [github.com](https://github.com).

**Step 2 —** Tap **Add file → Create new file**.

**Step 3 —** Name the file `gas_fee_estimator.py`

**Step 4 —** Paste the full code into the content area.

**Step 5 —** Write your commit message:
```
Add complete Ethereum gas fee estimator with EIP-1559 calculator, multi-chain comparison, speed tiers, daily cost estimator, live tracker simulation, and gas saving tips
