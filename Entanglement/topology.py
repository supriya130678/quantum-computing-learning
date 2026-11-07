import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx"])

def build_quantum_topology() -> nx.DiGraph:
    """
    Creates a sample quantum network graph with two alternative paths between S and D.
    
    Link attributes assigned:
      - F_i: Raw link fidelity (0.25 < F <= 1.0)
      - p_i: Entanglement generation success probability (0 < p <= 1.0)
      - r_i: Attempt rate in Hz (e.g., 10,000 Hz)
      - T_mem: Quantum memory coherence time in seconds (e.g., 0.01s = 10ms)
    """
    G = nx.DiGraph()
    
    # Path 1 Links (2 Hops - Short, but lower fidelity & lower success rate)
    G.add_edge("S", "N1", F_i=0.82, p_i=0.25, r_i=10000, T_mem=0.01)
    G.add_edge("N1", "D", F_i=0.82, p_i=0.25, r_i=10000, T_mem=0.01)
    
    # Path 2 Links (3 Hops - Longer, but high fidelity & fast generation)
    G.add_edge("S", "N2", F_i=0.98, p_i=0.80, r_i=10000, T_mem=0.01)
    G.add_edge("N2", "N3", F_i=0.97, p_i=0.85, r_i=10000, T_mem=0.01)
    G.add_edge("N3", "D", F_i=0.98, p_i=0.80, r_i=10000, T_mem=0.01)
    
    return G

if __name__ == "__main__":
    G = build_quantum_topology()
    print(f"Topology initialized with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")