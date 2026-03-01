# crypto_blockchain_basics.py
# A complete beginner's guide to Crypto & Blockchain concepts

from datetime import datetime
import hashlib
import json

# ──────────────────────────────────────────
# 1. Blockchain Concepts Dictionary
# ──────────────────────────────────────────
BLOCKCHAIN_CONCEPTS = {
    "Blockchain": (
        "A blockchain is a digital ledger that records transactions across "
        "many computers. Think of it like a Google Sheet that thousands of "
        "people have a copy of — no single person controls it, and every "
        "entry is permanent and transparent."
    ),
    "Block": (
        "A block is like a page in a notebook. It stores a group of "
        "transactions, a timestamp, and a unique code called a hash. "
        "Once a block is full, it gets added to the chain permanently."
    ),
    "Hash": (
        "A hash is a unique digital fingerprint. Every block has one. "
        "If even one character in a block changes, the entire hash changes — "
        "making tampering easy to detect."
    ),
    "Node": (
        "A node is any computer that participates in the blockchain network. "
        "Each node holds a full copy of the blockchain and helps verify "
        "new transactions."
    ),
    "Decentralization": (
        "Decentralization means no single authority controls the network. "
        "Instead of a bank managing your money, thousands of computers "
        "around the world validate and record every transaction."
    ),
    "Consensus Mechanism": (
        "This is the process by which all nodes agree on the valid state "
        "of the blockchain. The two most common are Proof of Work (PoW) "
        "and Proof of Stake (PoS)."
    ),
    "Smart Contract": (
        "A smart contract is a self-executing program stored on the blockchain. "
        "It automatically carries out an agreement when conditions are met — "
        "like a vending machine that releases a snack once you insert the "
        "right amount of money."
    ),
    "Wallet": (
        "A crypto wallet doesn't store coins — it stores your private keys. "
        "Think of it like a keychain. The coins live on the blockchain; "
        "your wallet just gives you access to them."
    ),
    "Private Key": (
        "Your private key is like your password and signature combined. "
        "It proves you own your crypto and allows you to send funds. "
        "NEVER share it with anyone — ever."
    ),
    "Public Key": (
        "Your public key is your crypto address — like your email address. "
        "You can share it freely so others can send you crypto."
    ),
    "Gas Fee": (
        "Gas fees are small payments made to compensate the network for "
        "processing your transaction. They vary based on network congestion — "
        "like surge pricing on a ride-sharing app."
    ),
    "DeFi": (
        "Decentralized Finance (DeFi) refers to financial services built on "
        "blockchain that operate without banks or intermediaries. You can "
        "lend, borrow, and earn interest using only your wallet."
    ),
    "NFT": (
        "A Non-Fungible Token (NFT) is a unique digital asset stored on the "
        "blockchain. Unlike Bitcoin where every coin is identical, each NFT "
        "is one-of-a-kind — like a digital certificate of ownership."
    ),
    "Altcoin": (
        "Any cryptocurrency that is not Bitcoin is called an altcoin. "
        "Examples include Ethereum, Solana, and Cardano. Each was created "
        "to solve specific problems or offer new features."
    ),
    "Stablecoin": (
        "A stablecoin is a cryptocurrency pegged to a stable asset like "
        "the US Dollar. Examples include USDT and USDC. They reduce "
        "volatility while keeping the benefits of crypto."
    )
}


# ──────────────────────────────────────────
# 2. Simple Block Simulation
# ──────────────────────────────────────────
class Block:
    """Simulates a basic blockchain block."""

    def __init__(self, index: int, data: str, previous_hash: str = "0"):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash[:20] + "...",
            "hash": self.hash[:20] + "..."
        }


# ──────────────────────────────────────────
# 3. Simple Blockchain Simulation
# ──────────────────────────────────────────
class SimpleBlockchain:
    """Simulates a basic blockchain."""

    def __init__(self):
        self.chain = [self._create_genesis_block()]

    def _create_genesis_block(self) -> Block:
        return Block(0, "Genesis Block — The First Block Ever", "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str) -> Block:
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def display_chain(self) -> None:
        for block in self.chain:
            print(json.dumps(block.to_dict(), indent=4))
            print("  ⬇ linked to")
        print("  [End of Chain]\n")


# ──────────────────────────────────────────
# 4. Crypto Types Overview
# ──────────────────────────────────────────
CRYPTO_TYPES = {
    "Store of Value": {
        "description": "Designed to hold value over time, like digital gold.",
        "examples": ["Bitcoin (BTC)"]
    },
    "Smart Contract Platform": {
        "description": "Supports decentralized apps and smart contracts.",
        "examples": ["Ethereum (ETH)", "Solana (SOL)", "Cardano (ADA)"]
    },
    "Stablecoins": {
        "description": "Pegged to real-world assets for price stability.",
        "examples": ["Tether (USDT)", "USD Coin (USDC)", "DAI"]
    },
    "DeFi Tokens": {
        "description": "Power decentralized finance platforms.",
        "examples": ["Uniswap (UNI)", "Aave (AAVE)", "Chainlink (LINK)"]
    },
    "Privacy Coins": {
        "description": "Focus on anonymous and private transactions.",
        "examples": ["Monero (XMR)", "Zcash (ZEC)"]
    },
    "Meme Coins": {
        "description": "Started as jokes but gained real communities.",
        "examples": ["Dogecoin (DOGE)", "Shiba Inu (SHIB)"]
    }
}


# ──────────────────────────────────────────
# 5. Beginner Mistakes to Avoid
# ──────────────────────────────────────────
BEGINNER_MISTAKES = [
    {
        "mistake": "Buying based on hype or social media.",
        "lesson": "Always research the project's whitepaper, team, and use case."
    },
    {
        "mistake": "Storing all crypto on an exchange.",
        "lesson": "Not your keys, not your coins. Use a personal wallet."
    },
    {
        "mistake": "Ignoring gas fees.",
        "lesson": "Always check fees before transacting, especially on Ethereum."
    },
    {
        "mistake": "Sending crypto to the wrong address.",
        "lesson": "Always double-check the full address. Transactions are irreversible."
    },
    {
        "mistake": "Falling for 'guaranteed returns' promises.",
        "lesson": "No legitimate project guarantees profits. It's always a scam."
    },
    {
        "mistake": "Using the same password everywhere.",
        "lesson": "Use a unique, strong password and a password manager."
    },
    {
        "mistake": "Panic selling during market dips.",
        "lesson": "Volatility is normal in crypto. Stick to your strategy."
    },
    {
        "mistake": "Not keeping records for tax purposes.",
        "lesson": "In most countries, crypto gains are taxable. Track every trade."
    }
]


# ──────────────────────────────────────────
# 6. How a Transaction Works (Step by Step)
# ──────────────────────────────────────────
def explain_transaction_flow() -> None:
    """Explains how a crypto transaction works step by step."""
    steps = [
        ("Step 1", "You initiate a transaction from your wallet."),
        ("Step 2", "The transaction is broadcast to the network of nodes."),
        ("Step 3", "Nodes verify that you have sufficient funds."),
        ("Step 4", "The transaction is grouped with others into a block."),
        ("Step 5", "Miners or validators confirm the block via consensus."),
        ("Step 6", "The confirmed block is added to the blockchain."),
        ("Step 7", "The recipient's wallet balance is updated."),
        ("Step 8", "The transaction is now permanent and irreversible.")
    ]

    print("\n  🔄 HOW A CRYPTO TRANSACTION WORKS")
    print("  " + "-" * 45)
    for step, description in steps:
        print(f"  {step}: {description}")


# ──────────────────────────────────────────
# 7. Display Functions
# ──────────────────────────────────────────
def display_concept(term: str) -> None:
    """Display explanation of a single blockchain concept."""
    if term in BLOCKCHAIN_CONCEPTS:
        print(f"\n  📖 {term}")
        print("  " + "-" * 40)
        print(f"  {BLOCKCHAIN_CONCEPTS[term]}")
    else:
        print(f"  ❌ Concept '{term}' not found.")


def display_all_concepts() -> None:
    """Display all blockchain concepts."""
    print("\n  📚 BLOCKCHAIN & CRYPTO CONCEPTS")
    print("  " + "=" * 45)
    for term, explanation in BLOCKCHAIN_CONCEPTS.items():
        print(f"\n  📖 {term}")
        print(f"  {explanation}")


def display_crypto_types() -> None:
    """Display types of cryptocurrencies."""
    print("\n  💰 TYPES OF CRYPTOCURRENCIES")
    print("  " + "=" * 45)
    for crypto_type, info in CRYPTO_TYPES.items():
        print(f"\n  🪙 {crypto_type}")
        print(f"  {info['description']}")
        print(f"  Examples: {', '.join(info['examples'])}")


def display_beginner_mistakes() -> None:
    """Display common beginner mistakes."""
    print("\n  ⚠️  COMMON BEGINNER MISTAKES & LESSONS")
    print("  " + "=" * 45)
    for i, item in enumerate(BEGINNER_MISTAKES, 1):
        print(f"\n  ❌ Mistake {i}: {item['mistake']}")
        print(f"  ✅ Lesson  : {item['lesson']}")


# ──────────────────────────────────────────
# 8. Main Runner
# ──────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("   🌐 Crypto & Blockchain Basics — Complete Beginner Guide")
    print("=" * 55)

    # Key concepts
    print("\n📌 SPOTLIGHT CONCEPTS:")
    for term in ["Blockchain", "Smart Contract", "DeFi", "Gas Fee"]:
        display_concept(term)

    # Transaction flow
    explain_transaction_flow()

    # Crypto types
    display_crypto_types()

    # Beginner mistakes
    display_beginner_mistakes()

    # Blockchain simulation
    print("\n\n📌 LIVE BLOCKCHAIN SIMULATION")
    print("  " + "=" * 45)
    blockchain = SimpleBlockchain()
    blockchain.add_block("Alice sends 0.5 BTC to Bob")
    blockchain.add_block("Bob sends 10 ETH to Carol")
    blockchain.add_block("Carol purchases an NFT for 2 SOL")

    print("\n  🔗 Current Blockchain State:")
    blockchain.display_chain()
    print(f"  ✅ Blockchain Valid: {blockchain.is_chain_valid()}")

    print("\n" + "=" * 55)
    print("  🎓 Beginner Guide Complete — Keep Learning!")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
```

---

**Step-by-Step Commit Guide on Mobile:**

**Step 1 —** Go to your `crypto-safety` repo on [github.com](https://github.com).

**Step 2 —** Tap **Add file → Create new file**.

**Step 3 —** Name the file `crypto_blockchain_basics.py`

**Step 4 —** Paste the full code into the content area.

**Step 5 —** Write your commit message:
```
Add complete beginner's guide to crypto and blockchain with concepts, live blockchain simulation, transaction flow, crypto types, and common mistakes
