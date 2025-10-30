import matplotlib.pyplot as plt
import json
import numpy as np

def plot_results():
    # Load results from JSON file
    try:
        with open('tsp_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: 'tsp_results.json' not found. Run 'main.py' first to generate results.")
        return
    
    test_cases = results['test_cases']
    es_avg_times = results['es_avg_times']
    hk_avg_times = results['hk_avg_times']
    nn_avg_times = results['nn_avg_times']
    es_best_costs = results['es_best_costs']
    hk_best_costs = results['hk_best_costs']
    nn_best_costs = results['nn_best_costs']
    es_extrapolated = results['es_extrapolated']
    hk_extrapolated = results['hk_extrapolated']
    nn_extrapolated = results['nn_extrapolated']
    max_feasible_es = results['max_feasible_es']
    max_feasible_hk = results['max_feasible_hk']
    
    fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, figsize=(12, 15))
    
   #log scale with extrapolation
    es_measured_n = [test_cases[i] for i in range(len(test_cases)) if es_avg_times[i] is not None]
    es_measured_times = [t for t in es_avg_times if t is not None]
    
    hk_measured_n = [test_cases[i] for i in range(len(test_cases)) if hk_avg_times[i] is not None]
    hk_measured_times = [t for t in hk_avg_times if t is not None]
    
    if es_measured_n:
        ax1.plot(es_measured_n, es_measured_times, 'ro-', linewidth=2, markersize=6, label='ES (measured)')
        ax1.plot(test_cases, es_extrapolated, 'r--', linewidth=1, label='ES (extrapolated)')
        ax1.axvline(x=max_feasible_es, color='red', linestyle=':', alpha=0.7, label=f'ES max feasible ({max_feasible_es})')
    
    if hk_measured_n:
        ax1.plot(hk_measured_n, hk_measured_times, 'gs-', linewidth=2, markersize=6, label='HK (measured)')
        ax1.plot(test_cases, hk_extrapolated, 'g--', linewidth=1, label='HK (extrapolated)')
        ax1.axvline(x=max_feasible_hk, color='green', linestyle=':', alpha=0.7, label=f'HK max feasible ({max_feasible_hk})')
    
    ax1.plot(test_cases, nn_avg_times, 'b^-', linewidth=2, markersize=6, label='GNN')
    
    ax1.set_xlabel('Number of Cities', fontsize=12)
    ax1.set_ylabel('Average Running Time (seconds)', fontsize=12)
    ax1.set_title('TSP Algorithm Running Times\n(Log Scale with Extrapolation)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    #linear scale for smaller values
    ax2.plot(test_cases, nn_avg_times, 'b^-', linewidth=2, markersize=6, label='GNN')
    
    if hk_measured_n:
        ax2.plot(hk_measured_n, hk_measured_times, 'gs-', linewidth=2, markersize=6, label='HK')
        ax2.axvline(x=max_feasible_hk, color='green', linestyle=':', alpha=0.7, label=f'HK max feasible ({max_feasible_hk})')
    
    if es_measured_n:
        ax2.plot(es_measured_n, es_measured_times, 'ro-', linewidth=2, markersize=6, label='ES')
        ax2.axvline(x=max_feasible_es, color='red', linestyle=':', alpha=0.7, label=f'ES max feasible ({max_feasible_es})')
    
    ax2.set_xlabel('Number of Cities', fontsize=12)
    ax2.set_ylabel('Average Running Time (seconds)', fontsize=12)
    ax2.set_title('TSP Algorithm Running Times\n(Linear Scale)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # solution cost comparison ( for overlapping instances)
    overlapping_cases = []
    es_costs_overlap = []
    hk_costs_overlap = []
    nn_costs_overlap = []
    
    for i, n in enumerate(test_cases):
        if es_best_costs[i] is not None and hk_best_costs[i] is not None:
            overlapping_cases.append(n)
            es_costs_overlap.append(es_best_costs[i])
            hk_costs_overlap.append(hk_best_costs[i])
            nn_costs_overlap.append(nn_best_costs[i])
    
    if overlapping_cases:
        width = 0.25
        x = np.arange(len(overlapping_cases))
        
        ax3.bar(x - width, es_costs_overlap, width, label='ES', color='red', alpha=0.7)
        ax3.bar(x, hk_costs_overlap, width, label='HK', color='green', alpha=0.7)
        ax3.bar(x + width, nn_costs_overlap, width, label='GNN', color='blue', alpha=0.7)
        
        ax3.set_xlabel('Number of Cities', fontsize=12)
        ax3.set_ylabel('Best Solution Cost', fontsize=12)
        ax3.set_title('Solution Cost Comparison\n(Overlapping Instances)', fontsize=14, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(overlapping_cases)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3, axis='y')
    else:
        ax3.text(0.5, 0.5, 'No overlapping instances\nfor cost comparison', 
                ha='center', va='center', transform=ax3.transAxes, fontsize=12)
        ax3.set_title('Solution Cost Comparison', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('tsp_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Maximum successfully terminated instances:")
    print(f"  Exhaustive Search: {max_feasible_es} cities")
    print(f"  Held-Karp: {max_feasible_hk} cities")
    print(f"  Greedy Nearest Neighbor: {max(test_cases)} cities")
    
    if overlapping_cases:
        print(f"\nOverlapping instances for cost comparison: {overlapping_cases}")
    
    print(f"\nExtrapolation method: Curve fitting based on known time complexities")
    print("  ES: O(n!) - factorial growth")
    print("  HK: O(n²·2ⁿ) - exponential growth") 
    print("  GNN: O(n²) - polynomial growth")
    print("\nPlots saved as 'tsp_comprehensive_analysis.png'")

if __name__ == '__main__':
    plot_results()