import pandas as pd
import numpy as np
from forecast import *
from optimize import *

if __name__ == "__main__":
    distance_matrix = pd.read_csv('../data/dataset/Distance_Matrix.csv')
    distance_matrix.drop(['Unnamed: 0'], axis=1, inplace=True)
    distance_matrix = np.array(distance_matrix)
    biomass_hist = pd.read_csv('../data/dataset/Biomass_History.csv')

    forecast_2018, forecast_2019 = forecast(distance_matrix, biomass_hist)
    # check for Constraint 1 (all forecasted values should be greater than 0)
    assert (all(x >= 0 for x in forecast_2018)),  "Constraint 1 failed for forecast 2018"
    assert (all(x >= 0 for x in forecast_2019)),  "Constraint 1 failed for forecast 2019"
    
    optimization_results = optimize(distance_matrix,[forecast_2018,forecast_2019])