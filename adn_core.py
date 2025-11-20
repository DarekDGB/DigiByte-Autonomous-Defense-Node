"""
DigiByte Autonomous Defense Node (ADN)
MIT Licensed — (c) 2025 DarekDGB

Self-running autonomous security agent for the DigiByte blockchain.
ADN continuously:
  - fetches local node statistics
  - analyzes risk via Sentinel AI + DQSN
  - executes automated defense actions
  - broadcasts alerts to operators
  - protects the node without human input
"""

import time
import json
import random
from dataclasses import dataclass
from typing import Dict, Optional

# -----------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------

ADN_VERSION = "1.0.0"

SENTINEL_ENDPOINT = "http://localhost:8000/sentinel/analyze"
DQSN_ENDPOINT = "http://localhost:8001/dqsnet/analyze"

CHECK_INTERVAL_SEC = 10        # how often ADN runs cycles
ALERT_THRESHOLD = 0.50         # anything above “high” triggers active defense
CRITICAL_THRESHOLD = 0.75      # triggers emergency defense

# -----------------------------------------------------------------------
# Data Models
# -----------------------------------------------------------------------

@dataclass
class NodeStats:
    mempool_count: int
    avg_block_interval: float
    last_block_entropy: float
    nonce_reuse_rate: float
    reorg_depth: int


@dataclass
class RiskResult:
    level: str
    score: float
    details: Dict


@dataclass
class DefenseAction:
    action: str
    reason: str


# -----------------------------------------------------------------------
# Mock Node Metrics (replace with real RPC later)
# -----------------------------------------------------------------------

def get_local_node_stats() -> NodeStats:
    """
    Placeholder for DigiByte RPC integration.
    Later this pulls mempool, block intervals, signatures, etc.
    """
    return NodeStats(
        mempool_count=random.randint(50, 500),
        avg_block_interval=random.uniform(12, 80),
        last_block_entropy=random.uniform(2.0, 8.0),
        nonce_reuse_rate=random.uniform(0.0, 0.05),
        reorg_depth=random.randint(0, 5),
    )


# -----------------------------------------------------------------------
# Risk Analysis Layer
# -----------------------------------------------------------------------

def analyze_risk(stats: NodeStats) -> RiskResult:
    """
    Simulates calling Sentinel AI + DQSN.
    In future releases this performs real HTTP requests.
    """
    # risk scoring is simplified here but mirrors sentinel/dqsnet structure
    entropy_risk = max(0.0, min(1.0, (8.0 - stats.last_block_entropy) / 8.0))
    nonce_risk = min(1.0, stats.nonce_reuse_rate * 20)
    reorg_risk = min(1.0, stats.reorg_depth / 4.0)
    mempool_risk = min(1.0, stats.mempool_count / 500)

    score = (
        entropy_risk * 0.30 +
        nonce_risk   * 0.25 +
        reorg_risk   * 0.25 +
        mempool_risk * 0.20
    )

    if score < 0.25:
        level = "normal"
    elif score < 0.50:
        level = "elevated"
    elif score < 0.75:
        level = "high"
    else:
        level = "critical"

    return RiskResult(
        level=level,
        score=round(score, 4),
        details={
            "entropy": entropy_risk,
            "nonce": nonce_risk,
            "reorg": reorg_risk,
            "mempool": mempool_risk,
        }
    )


# -----------------------------------------------------------------------
# Defense Engine
# -----------------------------------------------------------------------

def decide_defense_action(risk: RiskResult) -> Optional[DefenseAction]:
    if risk.score < ALERT_THRESHOLD:
        return None

    if risk.score >= CRITICAL_THRESHOLD:
        return DefenseAction(
            action="EMERGENCY_PQC_MIGRATION",
            reason="Critical quantum threat detected",
        )

    return DefenseAction(
        action="ROTATE_KEYS_AND_ALERT",
        reason="High risk level detected",
    )


def execute_defense(action: DefenseAction):
    """
    Executes the chosen defense move.
    These are placeholders; future versions interact with DigiByte node.
    """
    print(f"[ADN] Executing defense action: {action.action}")
    print(f"[ADN] Reason: {action.reason}")

    if action.action == "ROTATE_KEYS_AND_ALERT":
        print("[ADN] -> Rotating hot keys...")
        print("[ADN] -> Alert sent to operator channels")

    elif action.action == "EMERGENCY_PQC_MIGRATION":
        print("[ADN] -> Triggering emergency PQC migration...")
        print("[ADN] -> Locking non-essential operations")
        print("[ADN] -> Coordinating with Sentinel AI + DQSN")


# -----------------------------------------------------------------------
# Main Autonomous Loop
# -----------------------------------------------------------------------

def run_autonomous_loop():
    print(f"[ADN v{ADN_VERSION}] Autonomous defense loop running...")
    while True:
        stats = get_local_node_stats()
        print(f"\n[ADN] Node Stats: {stats}")

        risk = analyze_risk(stats)
        print(f"[ADN] Risk Score: {risk.score} | Level: {risk.level}")

        action = decide_defense_action(risk)
        if action:
            execute_defense(action)
        else:
            print("[ADN] No defense needed this cycle.")

        time.sleep(CHECK_INTERVAL_SEC)


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------

if __name__ == "__main__":
    run_autonomous_loop()
