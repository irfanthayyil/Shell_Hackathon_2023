import pandas as pd

def create_submission(forecast_2018, forecast_2019, optimization_results):
    sample = pd.read_csv('../../data/dataset/sample_submission.csv')
    sub = pd.DataFrame(columns=sample.columns)
    depots_used, refineries_used, biomass_source_index, biomass_destination_index, biomass_flow, pellet_source_index, pellet_destination_index, pellet_flow = optimization_results
    #TODO
    # biomass_flow_2019 = 
    # pellet_flow_2019 = 
    NUMBER_OF_DEPOTS = len(depots_used) 
    NUMBER_OF_REFINERIES = len(refineries_used) 
  
    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [20182019]*NUMBER_OF_DEPOTS
    df1['data_type'] = ['depot_location']*NUMBER_OF_DEPOTS
    df1['source_index'] = depots_used 

    sub = pd.concat([sub,df1])

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [20182019]*NUMBER_OF_REFINERIES
    df1['data_type'] = ['refinery_location']*NUMBER_OF_REFINERIES
    df1['source_index'] = refineries_used

    sub = pd.concat([sub,df1])

    NUMBER_OF_LOCATIONS =2418
   
    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2018]*NUMBER_OF_LOCATIONS
    df1['data_type'] = ['biomass_forecast']*NUMBER_OF_LOCATIONS
    df1['source_index'] = [i for i in range(NUMBER_OF_LOCATIONS)]
    df1['value'] = forecast_2018

    sub = pd.concat([sub,df1])

    assert len(biomass_source_index) == len(biomass_destination_index)

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2018]*len(biomass_source_index)
    df1['data_type'] = ['biomass_demand_supply']*len(biomass_source_index)
    df1['source_index'] = biomass_source_index
    df1['destination_index'] = biomass_destination_index
    df1['value'] = biomass_flow

    sub = pd.concat([sub,df1])


    assert len(pellet_source_index) == len(pellet_destination_index)

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2018]*len(pellet_destination_index)
    df1['data_type'] = ['pellet_demand_supply']*len(pellet_destination_index)
    df1['source_index'] = pellet_source_index
    df1['destination_index'] = pellet_destination_index
    df1['value'] = pellet_flow

    sub = pd.concat([sub,df1])

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2019]*NUMBER_OF_LOCATIONS
    df1['data_type'] = ['biomass_forecast']*NUMBER_OF_LOCATIONS
    df1['source_index'] = [i for i in range(NUMBER_OF_LOCATIONS)]
    df1['value'] = forecast_2019
    
    sub = pd.concat([sub,df1])

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2019]*len(biomass_source_index)
    df1['data_type'] = ['biomass_demand_supply']*len(biomass_source_index)
    df1['source_index'] = biomass_source_index
    df1['destination_index'] = biomass_destination_index
    #TODO
    # df1['value'] = biomass_flow_2019

    sub = pd.concat([sub,df1])

    df1 = pd.DataFrame(columns=sample.columns)
    df1['year'] = [2019]*len(pellet_destination_index)
    df1['data_type'] = ['pellet_demand_supply']*len(pellet_destination_index)
    df1['source_index'] = pellet_source_index
    df1['destination_index'] = pellet_destination_index
    #TODO:
    #df1['value'] = pellet_flow_2019

    sub = pd.concat([sub,df1])

    sub.reset_index(drop=True, inplace=True)
    sub.to_csv('../../outputs/submission.csv', index=False)