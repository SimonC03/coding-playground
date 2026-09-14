using JuMP
import Ipopt
using Printf

include("project_data.jl")

# Sets
N = nodes        # N: set of nodes {1,...,11}
E = edges        # E ⊆ N×N: set of transmission lines {(1,2),...,(10,11)}
G = generators   # G: set of generators {1,...,9}
C = consumers    # C: set of consumers {1,...,7}

N_k = [Int[] for k in N]   # N(k): neighbours of node k
for (k, ℓ) in E
    push!(N_k[k], ℓ)
    push!(N_k[ℓ], k)
end
G_k = [[i for i in G if gen_node[i] == k] for k in N]   # G_k: generators in node k
C_k = [[j for j in C if con_node[j] == k] for k in N]   # C_k: consumers in node k

# Parameters
c = gen_cost                 # c_i: production cost for generator i [SEK/pu]
P_max = gen_cap              # P_i^max: max capacity for generator i [pu]
d = con_demand               # d_j: demand from consumer j [pu]
V_min, V_max = v_min, v_max  # V^min, V^max: limits for voltage [vu]
α = q_share                  # α: share of capacity usable for reactive power

# b_kℓ = b_ℓk and g_kℓ = g_ℓk: parameters describing the edges
b = zeros(length(N), length(N))
g = zeros(length(N), length(N))
for (e, (k, ℓ)) in enumerate(E)
    b[k, ℓ] = b[ℓ, k] = b_edge[e]
    g[k, ℓ] = g[ℓ, k] = g_edge[e]
end

model = Model(Ipopt.Optimizer)

# Variables
@variable(model, 0 <= G_p[i in G] <= P_max[i])                  # G_i^P: active power from generator i [pu]
@variable(model, -α * P_max[i] <= G_q[i in G] <= α * P_max[i])  # G_i^q: reactive power, >0 producing, <0 absorbing [pu]
@variable(model, V_min <= v[k in N] <= V_max, start = 1.0)      # v_k: voltage amplitude in node k [vu]
@variable(model, -π <= θ[k in N] <= π, start = 0.0)             # θ_k: phase angle in node k [rad]
@variable(model, p[k in N, ℓ in N_k[k]])                        # p_kℓ: active power from k to ℓ [pu]
@variable(model, q[k in N, ℓ in N_k[k]])                        # q_kℓ: reactive power from k to ℓ [pu]

# Objective
@objective(model, Min, sum(c[i] * G_p[i] for i in G))

# Constraints
@constraint(model, active_flow[k in N, ℓ in N_k[k]],
    p[k, ℓ] == v[k]^2 * g[k, ℓ] - v[k] * v[ℓ] * g[k, ℓ] * cos(θ[k] - θ[ℓ]) -
               v[k] * v[ℓ] * b[k, ℓ] * sin(θ[k] - θ[ℓ]))
@constraint(model, reactive_flow[k in N, ℓ in N_k[k]],
    q[k, ℓ] == -v[k]^2 * b[k, ℓ] + v[k] * v[ℓ] * b[k, ℓ] * cos(θ[k] - θ[ℓ]) -
               v[k] * v[ℓ] * g[k, ℓ] * sin(θ[k] - θ[ℓ]))
@constraint(model, active_balance[k in N],
    sum(G_p[i] for i in G_k[k]) - sum(d[j] for j in C_k[k]) == sum(p[k, ℓ] for ℓ in N_k[k]))
@constraint(model, reactive_balance[k in N],
    sum(G_q[i] for i in G_k[k]) == sum(q[k, ℓ] for ℓ in N_k[k]))

optimize!(model)

# Results
println("Termination status: ", termination_status(model))
@printf("Total cost: %.4f SEK\n", objective_value(model))

println("\nGenerator  node   G_p [pu]   G_q [pu]")
for i in G
    @printf("G%-8d %4d %10.4f %10.4f\n", i, gen_node[i], value(G_p[i]), value(G_q[i]))
end

println("\nNode   v [vu]   θ [rad]")
for k in N
    @printf("%4d %8.4f %9.4f\n", k, value(v[k]), value(θ[k]))
end

println("\nEdge (k,ℓ)   p_kℓ [pu]   q_kℓ [pu]")
for k in N, ℓ in N_k[k]
    @printf("(%2d,%2d) %12.4f %11.4f\n", k, ℓ, value(p[k, ℓ]), value(q[k, ℓ]))
end
