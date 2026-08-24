import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import scipy.stats as stats
import os

os.makedirs('experiments/plots', exist_ok=True)
os.makedirs('experiments/results', exist_ok=True)

sns.set_theme(style="whitegrid")

def plot_h1():
    print("Plotting H1...")
    df = pd.read_csv('experiments/raw/H1_detection_results.csv')
    
    # 1. Plot trust score over time for H1-D (Sudden Degradation)
    plt.figure(figsize=(10, 6))
    h1d = df[df['scenario'] == 'H1-D'].groupby('time_step')['T_i'].mean().reset_index()
    sns.lineplot(data=h1d, x='time_step', y='T_i', label='Trust Score $T_i(t)$')
    plt.axvline(50, color='r', linestyle='--', label='Degradation Point')
    plt.axhline(0.5, color='orange', linestyle=':', label='Quarantine Threshold')
    plt.title('H1-D: Trust Score Response to Sudden Degradation')
    plt.xlabel('Time Step')
    plt.ylabel('Trust Score')
    plt.legend()
    plt.savefig('experiments/plots/H1_degradation_response.png')
    plt.close()
    
    # 2. Compute Precision, Recall, F1
    # We want to detect 'ground_truth_bad' == True.
    # Prediction is Positive if trust_state_b3 == 'QUARANTINED'
    # For B1, Prediction is always Negative (TRUSTED), so it never detects bad behavior.
    
    # We will compute metrics across all rows (time steps) to see overall classification
    y_true = df['ground_truth_bad']
    y_pred_b3 = (df['trust_state_b3'] == 'QUARANTINED')
    y_pred_b1 = (df['trust_state_b1'] == 'QUARANTINED') # Always false
    
    f1_b3 = f1_score(y_true, y_pred_b3)
    f1_b1 = f1_score(y_true, y_pred_b1)
    
    print(f"H1 F1-Score: B3(TrustChain)={f1_b3:.3f}, B1(Static)={f1_b1:.3f}")
    
    # Detection Time for H1-D
    # For each run, find the first time_step > 50 where state == QUARANTINED
    det_times = []
    for run_id in df[df['scenario'] == 'H1-D']['run_id'].unique():
        run_data = df[(df['scenario'] == 'H1-D') & (df['run_id'] == run_id) & (df['time_step'] >= 50)]
        quarantined = run_data[run_data['trust_state_b3'] == 'QUARANTINED']
        if not quarantined.empty:
            det_time = quarantined['time_step'].min() - 50
            det_times.append(det_time)
    
    mean_det = np.mean(det_times)
    std_det = np.std(det_times)
    print(f"H1-D Detection Time: {mean_det:.2f} ± {std_det:.2f} steps")
    
    with open('experiments/results/H1_stats.txt', 'w') as f:
        f.write(f"B3 F1-Score: {f1_b3:.3f}\n")
        f.write(f"B1 F1-Score: {f1_b1:.3f}\n")
        f.write(f"Detection Time: {mean_det:.2f} ± {std_det:.2f} steps\n")

def plot_h2():
    print("Plotting H2...")
    df = pd.read_csv('experiments/raw/H2_ablation_results.csv')
    
    results = []
    for ablation in df['ablation'].unique():
        sub_df = df[df['ablation'] == ablation]
        y_true = sub_df['ground_truth_bad']
        y_pred = (sub_df['trust_state_b3'] == 'QUARANTINED')
        f1 = f1_score(y_true, y_pred)
        results.append({'Ablation': ablation, 'F1-Score': f1})
        
    res_df = pd.DataFrame(results)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=res_df, x='Ablation', y='F1-Score')
    plt.title('H2: Ablation Study on Behavioral Signals')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('experiments/plots/H2_ablation_f1.png')
    plt.close()
    
    res_df.to_csv('experiments/results/H2_stats.csv', index=False)
    print(res_df)

def plot_h3():
    print("Plotting H3...")
    df = pd.read_csv('experiments/raw/H3_lambda_results.csv')
    
    plt.figure(figsize=(12, 6))
    h1d = df[df['scenario'] == 'H1-D'].groupby(['time_step', 'lambda'])['T_i'].mean().reset_index()
    sns.lineplot(data=h1d, x='time_step', y='T_i', hue='lambda', palette='viridis')
    plt.axvline(50, color='r', linestyle='--', label='Degradation Point')
    plt.axhline(0.5, color='orange', linestyle=':', label='Quarantine')
    plt.title('H3: Temporal Trust Responsiveness by Lambda')
    plt.legend()
    plt.savefig('experiments/plots/H3_lambda_response.png')
    plt.close()
    
def plot_scale():
    print("Plotting Scalability...")
    df = pd.read_csv('experiments/raw/Scale_results.csv')
    
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='population', y='ms_per_event', marker='o')
    plt.title('H5: SQLite VDR Processing Overhead')
    plt.xlabel('Agent Population')
    plt.ylabel('Processing Time per Event (ms)')
    plt.ylim(0, max(df['ms_per_event'])*1.2)
    plt.savefig('experiments/plots/H5_scalability.png')
    plt.close()

if __name__ == "__main__":
    plot_h1()
    plot_h2()
    plot_h3()
    plot_scale()
    print("Plotting completed.")
