import pandas as pd
import numpy as np
import uuid
import os
import random
import json
import sqlite3
import time
from datetime import datetime, timezone

from akta.telemetry import TelemetryEvent, TestHarnessTelemetrySource
from akta.vdr.database import Base, engine, SessionLocal
from akta.vdr import trust_crud
from akta.vdr import models
from akta.trust_engine import TrustConfig, TrustState

os.makedirs('experiments/configs', exist_ok=True)
os.makedirs('experiments/raw', exist_ok=True)

DEFAULT_CONFIG = {
    "w1": 0.6,
    "w2": 0.3,
    "w3": 0.1,
    "lam": 0.7,
    "trusted_threshold": 0.8,
    "suspicious_threshold": 0.5,
    "max_latency_ms": 1000,
    "number_of_runs": 30
}
with open('experiments/configs/default_config.json', 'w') as f:
    json.dump(DEFAULT_CONFIG, f, indent=4)

Base.metadata.create_all(bind=engine)

def get_config():
    with open('experiments/configs/default_config.json', 'r') as f:
        return json.load(f)

def run_h1(config):
    db = SessionLocal()
    # just clear db for isolation
    db.execute(Base.metadata.tables['agent_trust_states'].delete())
    db.execute(Base.metadata.tables['telemetry_logs'].delete())
    db.execute(Base.metadata.tables['trust_audit_trails'].delete())
    db.commit()

    source = TestHarnessTelemetrySource()
    results = []
    
    # We will simulate 30 runs of 100 time steps each, across 6 scenarios.
    # We won't simulate all 18,000 steps since it takes too long, maybe just 1 run for demonstration here to keep it fast, 
    # but the prompt says 30 runs. It took 3 seconds for 500 events in H5. So 18,000 might take 2 minutes. Let's do it.
    
    # Simplified simulation to save time but adhere to requirements
    scenarios = ["H1-A", "H1-B", "H1-C", "H1-D", "H1-E", "H1-F"]
    
    for scenario in scenarios:
        for run_id in range(config['number_of_runs']):
            seed = 1000 + run_id * 7
            random.seed(seed)
            agent_did = f"did:key:agent_{scenario}_{run_id}"
            
            for t in range(100):
                is_bad = False
                success = True
                compliance = False # meaning no violation
                latency = random.randint(10, 100)
                
                if scenario == "H1-B": # repeated failures
                    is_bad = True
                    success = False
                elif scenario == "H1-C": # protocol violations
                    is_bad = True
                    compliance = True
                elif scenario == "H1-D": # sudden degradation at t=50
                    if t >= 50:
                        is_bad = True
                        success = False
                elif scenario == "H1-E": # mixed failures
                    is_bad = True
                    success = random.choice([True, False])
                    compliance = random.choice([True, False])
                    latency = random.randint(500, 2500)
                elif scenario == "H1-F": # recovery after degradation
                    if 30 <= t < 70:
                        is_bad = True
                        success = False
                        
                raw = {
                    "agent_did": agent_did,
                    "task_id": str(uuid.uuid4()),
                    "success": success,
                    "compliance_event": compliance,
                    "latency_ms": latency,
                    "timestamp": datetime.now(timezone.utc).timestamp()
                }
                
                # B1 (Static): Always returns TRUSTED (False for QUARANTINED)
                state_b1 = 'TRUSTED'
                
                # B3 (TrustChain)
                event = source.ingest(raw)
                # Override trust engine config
                trust_crud.trust_engine.config = TrustConfig(**config)
                new_state = trust_crud.record_telemetry_and_update_trust(db, event)
                
                results.append({
                    "run_id": run_id,
                    "seed": seed,
                    "scenario": scenario,
                    "agent_did": agent_did,
                    "time_step": t,
                    "ground_truth_bad": is_bad,
                    "S_i": trust_crud.trust_engine.calculate_S_i([event]), # Approx point-in-time
                    "C_i": trust_crud.trust_engine.calculate_C_i([event]),
                    "L_i": trust_crud.trust_engine.calculate_L_i([event]),
                    "T_i": new_state.temporal_trust_score,
                    "trust_state_b1": state_b1,
                    "trust_state_b3": new_state.trust_state
                })
    
    df = pd.DataFrame(results)
    df.to_csv('experiments/raw/H1_detection_results.csv', index=False)
    db.close()
    
def run_all():
    print("Running experiments based on default config...")
    config = get_config()
    run_h1(config)
    print("Experiments complete.")

if __name__ == "__main__":
    run_all()
