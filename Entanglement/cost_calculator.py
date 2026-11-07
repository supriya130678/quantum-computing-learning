import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx"])
import math

def calculate_depolarizing_parameter(F_i: float) -> float:
    """Calculates depolarizing parameter w_i = (4 * F_i - 1) / 3"""
    if F_i <= 0.25 or F_i > 1.0:
        raise ValueError(f"Fidelity F_i must be in range (0.25, 1.0], got {F_i}")
    return (4.0 * F_i - 1.0) / 3.0

def calculate_generation_time(p_i: float, r_i: float) -> float:
    """Calculates average entanglement generation time t_i = 1 / (p_i * r_i)"""
    if p_i <= 0 or r_i <= 0:
        raise ValueError("Success probability p_i and attempt rate r_i must be positive.")
    return 1.0 / (p_i * r_i)

def calculate_link_cost(F_i: float, p_i: float, r_i: float, T_mem: float,alpha: float = 1.0, beta: float = 1.0, gamma: float = 0.1) -> dict:
    """
    Calculates composite link cost breakdown:
    c_i = alpha * [-ln(w_i)] + beta * (t_i / T_mem) + gamma
    """
    w_i = calculate_depolarizing_parameter(F_i)
    t_i = calculate_generation_time(p_i, r_i)
    
    cost_fidelity = alpha * (-math.log(w_i))
    cost_decoherence = beta * (t_i / T_mem)
    cost_hop = gamma
    
    total_cost = cost_fidelity + cost_decoherence + cost_hop
    
    return {
        "w_i": w_i,
        "t_i": t_i,
        "cost_fidelity": cost_fidelity,
        "cost_decoherence": cost_decoherence,
        "cost_hop": cost_hop,
        "total_cost": total_cost
    }

def compute_graph_costs(G: nx.DiGraph, alpha: float = 1.0, beta: float = 1.0, gamma: float = 0.1) -> nx.DiGraph:
    """Annotates all graph edges with link cost components and sets 'weight' = total_cost."""
    for u, v, data in G.edges(data=True):
        metrics = calculate_link_cost(
            F_i=data["F_i"],
            p_i=data["p_i"],
            r_i=data["r_i"],
            T_mem=data["T_mem"],
            alpha=alpha,
            beta=beta,
            gamma=gamma
        )
        data.update(metrics)
        data["weight"] = metrics["total_cost"]
    return G

if __name__ == "__main__":
    from topology import build_quantum_topology
    G = compute_graph_costs(build_quantum_topology())
    for u, v, d in G.edges(data=True):
        print(f"Edge ({u} -> {v}): Weight={d['weight']:.4f} | FidelityCost={d['cost_fidelity']:.4f} | LatencyCost={d['cost_decoherence']:.4f}")