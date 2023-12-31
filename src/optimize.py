import pandas as pd
import numpy as np
from pyomo.environ import *

# distance_matrix = pd.read_csv('../data/dataset/Distance_Matrix.csv')
# biomass_hist = pd.read_csv('../data/dataset/Biomass_History.csv')

# distance_matrix.drop(['Unnamed: 0'], axis=1, inplace=True)
# distance_matrix = np.array(distance_matrix)

# b_2010 = np.array(biomass_hist['2010'])

def optimize(distance_matrix, harvests,num_locations = 2418,num_depots_max = 25,num_refineries_max = 5,cap_depot = 20000,cap_refinery = 100000, hotspot_indices=None):
       
    #TODO: Harvest needs to be list of lists, (for every year)
    # Create a concrete model
    harvest = harvests[0]
    model = ConcreteModel()
    # Index sets
    print("Setting Decision Variables...")
    if hotspot_indices == None:
        model.locations = RangeSet(num_locations)
        model.depots = RangeSet(num_locations)  # We assume all locations can be potential depots
        model.refineries = RangeSet(num_locations) # We assume all locations can be potential refineries
    else:
        model.locations = RangeSet(num_locations) 
        model.depots = Set(initialize=hotspot_indices)  # Consider only the hotspot indices
        model.refineries = Set(initialize=hotspot_indices)  # Consider only the hotspot indices
    # Decision variables
    model.depots_used = Var(model.depots, within=Binary)
    model.refineries_used = Var(model.refineries, within=Binary)
    model.harvest_flow = Var(model.locations, model.depots, within=NonNegativeReals) # *Constraint 1
    model.pellet_flow = Var(model.depots, model.refineries, within=NonNegativeReals) # *Constraint 1
    # model.under_utilization_cost = Var(model.depots, within=NonNegativeReals)
    # model.under_utilization_cost_refineries = Var(model.refineries, within=NonNegativeReals)
    # model.pellet_flow_active = Var(model.depots, model.refineries, within=Binary)  # Binary variable indicating active pellet flow
    print("Setting Objective Function...")
    ## Linear

    # Objective function
    def objective_rule(model):
        return (
            0.001*sum(distance_matrix[i-1][j-1] * model.harvest_flow[i, j] for i in model.locations for j in model.depots) +
            0.001*sum(distance_matrix[j-1][k-1] * model.pellet_flow[j, k] for j in model.depots for k in model.refineries) +
            sum(cap_depot - model.harvest_flow[i, j] for i in model.locations for j in model.depots) +  # Under-utilization cost for depots
            sum(cap_refinery - model.pellet_flow[j, k] for j in model.depots for k in model.refineries)   # Under-utilization cost for refineries
            # sum(cap_refinery * (1 - model.refineries_used[k]) for k in model.refineries)  # Under-utilization cost for unused refineries -->redundant
        )
    model.objective = Objective(rule=objective_rule, sense=minimize)


    ## Non Linear
    # Objective function
    
    # def objective_rule(model):
    #     return (
    #         0.001*sum(distance_matrix[i-1][j-1]*model.harvest_flow[i, j]*model.depots_used[j] for i in model.locations for j in model.depots) +
    #         0.001*sum(distance_matrix[j-1][k-1]*model.pellet_flow[j, k]*model.depots_used[j] *model.refineries_used[k]  for j in model.depots for k in model.refineries) +
    #         sum(cap_depot - model.harvest_flow[i, j] for i in model.locations for j in model.depots) +  # Under-utilization cost for depots
    #         sum(cap_refinery - model.pellet_flow[j, k] for j in model.depots for k in model.refineries)   # Under-utilization cost for refineries
    #     )
    # model.objective = Objective(rule=objective_rule, sense=minimize)


    # Constraints
    print("Setting Constraints...")
    # * Constraint 2
    def harvest_supply_constraint_rule(model, i):
        return sum(model.harvest_flow[i, j] for j in model.depots) <= harvest[i-1]
    model.harvest_supply_constraint = Constraint(model.locations, rule=harvest_supply_constraint_rule)

    # * Constraint 3 
    # for maximum utilization of a Depot
    def max_utilization_constraint_rule(model, j):
        return sum(model.harvest_flow[i, j] for i in model.locations) <= cap_depot
    model.max_utilization_constraint = Constraint(model.depots, rule=max_utilization_constraint_rule)

    # * Constraint 4 
    # for maximum utilization of a refinery
    def max_utilization_refineries_constraint_rule(model, k):
        return sum(model.pellet_flow[j, k] for j in model.depots) <= cap_refinery
    model.max_utilization_refineries_constraint = Constraint(model.refineries, rule=max_utilization_refineries_constraint_rule)

    # *Constraint 5
    def max_depots_constraint_rule(model):
        return sum(model.depots_used[j] for j in model.depots) <= num_depots_max
    model.max_depots_constraint = Constraint(rule=max_depots_constraint_rule)

    # * Constraint 6
    # Constraint for maximum number of refineries
    def max_refineries_constraint_rule(model):
        return sum(model.refineries_used[k] for k in model.refineries) <= num_refineries_max
    model.max_refineries_constraint = Constraint(rule=max_refineries_constraint_rule)

    # * Constraint 7
    # At least 80% of the total forecasted biomass must be processed by refineries each year
    def min_80_constraint_rule(model):
        return sum(model.pellet_flow[j, k] for j in model.depots for k in model.refineries) >= 0.8*sum(harvest)
    model.min_80_constraint = Constraint(rule=min_80_constraint_rule)

    # * Constraint 8
    # Constraint for pellets flow balance
    def pellet_flow_balance_rule(model, j):
        return (
            sum(model.pellet_flow[j, k] for k in model.refineries) - sum(model.harvest_flow[i, j] for i in model.locations) <= 1e-03
        )
    model.pellet_flow_balance_constraint = Constraint(model.depots, rule=pellet_flow_balance_rule)

    def flow_binary_relation_rule(model, i, j):
        """
        This constraint ensures that if a depot is used (the binary variable is 1), 
        the corresponding harvest flow can be non-zero, but if a depot is not used (the binary variable is 0), the corresponding harvest flow must be zero.
        """
        return model.harvest_flow[i, j] <= model.depots_used[j] * harvest[i-1]
    model.flow_binary_relation_constraint = Constraint(model.locations, model.depots, rule=flow_binary_relation_rule)

    def pellet_flow_binary_relation_rule(model,j, k):
        return model.pellet_flow[j, k] <= model.refineries_used[k] * sum(model.harvest_flow[i, j] for i in model.locations)
    model.pellet_flow_binary_relation_constraint = Constraint(model.depots, model.refineries, rule=pellet_flow_binary_relation_rule)


    # Solve the problem
    print("Solution started...")
    solver = SolverFactory('ipopt')
    results = solver.solve(model)

    # Display results
    print("Solver status:", results.solver.status)
    print("Objective value:", value(model.objective))

    depots_used = [j for j in model.depots if value(model.depots_used[j]) > 0.5]
    # print("Depot locations:", depots_used)
    refineries_used = [k for k in model.refineries if value(model.refineries_used[k]) > 0.5]
    # print("Refineries locations:", refineries_used)

    biomass_source_index = []
    biomass_destination_index = []
    biomass_flow = []
    for i in model.locations:
        for j in depots_used:
            f = value(model.harvest_flow[i, j])
            if f > 0:
                biomass_source_index.append(i)
                biomass_destination_index.append(j)
                biomass_flow.append(f)

    assert (all(x >= 0 for x in biomass_flow)),  "Constraint 1 failed for biomass demand supply"
    
    pellet_source_index = []
    pellet_destination_index = []
    pellet_flow = []
    for i in model.locations:
        for j in refineries_used:
            f = value(model.pellet_flow[i, j])
            if f > 0:
                pellet_source_index.append(i)
                pellet_destination_index.append(j)
                pellet_flow.append(f)
                
    assert (all(x >= 0 for x in pellet_flow)),  "Constraint 1 failed for pellet demand supply"

    return [depots_used, refineries_used, biomass_source_index, biomass_destination_index, biomass_flow, pellet_source_index, pellet_destination_index, pellet_flow]