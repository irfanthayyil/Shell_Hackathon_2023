import pandas as pd
import numpy as np
from forecast import *
from optimize import *

if __name__ == "__main__":
    distance_matrix = pd.read_csv('../data/dataset/Distance_Matrix.csv')
    distance_matrix.drop(['Unnamed: 0'], axis=1, inplace=True)
    distance_matrix = np.array(distance_matrix)
    biomass_hist = pd.read_csv('../data/dataset/Biomass_History.csv')
    biomass_hist["mean_by_year"] = biomass_hist.iloc[:, 3:].mean(axis=1)
    mean_harvest= np.array(biomass_hist['mean_by_year'])

    # forecast_2018, forecast_2019 = forecast(distance_matrix, biomass_hist)
    # # check for Constraint 1 (all forecasted values should be greater than 0)
    # assert (all(x >= 0 for x in forecast_2018)),  "Constraint 1 failed for forecast 2018"
    # assert (all(x >= 0 for x in forecast_2019)),  "Constraint 1 failed for forecast 2019"

    hotspot_indices = []
    with open('../outputs/indices_48.txt') as f:
        for x in f:
            hotspot_indices.append(int(x.split('\n')[0]))

    
    # optimization_results = optimize(distance_matrix,[forecast_2018,forecast_2019])
    optimization_results = optimize(distance_matrix,[mean_harvest], hotspot_indices=hotspot_indices)
    depots_used, refineries_used, biomass_source_index, biomass_destination_index, biomass_flow, pellet_source_index, pellet_destination_index, pellet_flow = optimization_results
    
    with open('../outputs/depots_used.txt',"w") as fp:
        for item in depots_used:
            fp.write("%s\n" %item)
    print("Depots Saved")
    
    with open('../outputs/refineries_used.txt',"w") as fp:
        for item in refineries_used:
            fp.write("%s\n" %item)
    print("refineries_used Saved")
    
    with open('../outputs/biomass_source_index.txt',"w") as fp:
        for item in biomass_source_index:
            fp.write("%s\n" %item)
    print("biomass_source_index Saved")
    
    with open('../outputs/biomass_destination_index.txt',"w") as fp:
        for item in biomass_destination_index:
            fp.write("%s\n" %item)
    print("biomass_destination_index Saved")
    
    with open('../outputs/biomass_flow.txt',"w") as fp:
        for item in biomass_flow:
            fp.write("%s\n" %item)
    print("biomass_flow Saved")
    
    with open('../outputs/pellet_source_index.txt',"w") as fp:
        for item in pellet_source_index:
            fp.write("%s\n" %item)
    print("pellet_source_index Saved")
    
    with open('../outputs/pellet_destination_index.txt',"w") as fp:
        for item in pellet_destination_index:
            fp.write("%s\n" %item)
    print("pellet_destination_index Saved")
    with open('../outputs/pellet_destination_index.txt',"w") as fp:
        for item in pellet_destination_index:
            fp.write("%s\n" %item)         
    print("pellet_destination_index Saved")

    with open('../outputs/pellet_flow.txt',"w") as fp:
        for item in pellet_flow:
            fp.write("%s\n" %item)
    print("pellet_flow Saved")
