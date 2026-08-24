import os

dirs = [
    "experiments/configs",
    "experiments/scenarios",
    "experiments/runners",
    "experiments/metrics",
    "experiments/results",
    "experiments/raw",
    "experiments/plots"
]

for d in dirs:
    os.makedirs(f"d:/capstone project/trustchain-ai/akta-base/{d}", exist_ok=True)
