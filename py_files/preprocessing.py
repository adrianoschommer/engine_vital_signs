
import pandas as pd
import numpy as np
#from read_data import read_data
import os
import export.config
#from filter_data import filter_data
main_wd = export.config.main_wd



def preprocessing(target_folder):
    """This function returns a DataFrame cointaining the reference points and key indicators
    
    Keyword arguments:
    target_folder -- path to the folder containing the .prn files of the session of interest
    """  
    database = export.read_data(target_folder, main_wd)
    reference_point = pd.DataFrame()
    vehicles = database.Vehicle.unique() # stores into a list all unique vehicle strings

    for vehicle in vehicles:
        # Restores database before filtering.
        data = database 

        # Gets vehicle data currently in the loop.
        data = data[data.Vehicle == str(vehicle)]   

        # Identify which baseline TPS is being used in the race event, it might differ from season to season.
        # It also has to consider the push to pass feature, wich for a limited amount of time give 100% of TPS.
        average_TPS = np.average(database[(database['TPS'] < export.config.max_TPS) & 
                                          (database['Pdl'] > export.config.min_Pdl) & 
                                          (database['VehicleSpeed'] > export.config.min_VehicleSpeed)]['TPS'])  

        # Thresholds used to target the reference point
        threshold = {'Gear_Pot':export.config.thld_1_Gear_Pot, 
                     'TPS':(average_TPS*(1-export.config.thld_1_TPS),average_TPS*(1+export.config.thld_1_TPS)), 
                     'Pdl':export.config.thld_1_Pdl, 
                     'RPM':export.config.thld_1_RPM}  
        reference_point = reference_point.append(export.filter_data(data, threshold, vehicle).iloc[-1,:])

        # Thresholds used to get min and max values from the entire outing (i.e. not at the reference point).
        threshold_min_max = {'Gear_Pot':export.config.thld_2_Gear_Pot, 
                             'TPS':(average_TPS*(1-export.config.thld_2_TPS),export.config.thld_2_max_TPS), 
                             'Pdl':export.config.thld_2_Pdl, 
                             'RPM':export.config.thld_2_RPM}
        data = export.filter_data(data, threshold_min_max, vehicle)  

        # Target parameters to append min and max values.
        parameters_dict = {'Min_P_Oil':min(data['P_Oil']), 
                           'Max_T_Water':max(data['T_Water']), 
                           'Max_T_Oil':max(data['T_Oil']),
                           'Min_P_Fuel':min(data['P_Fuel']), 
                           'Max_VehicleSpeed':max(data['VehicleSpeed']), 
                           'Max_TPS':max(data['TPS'])}

        # Search for the Vechile currently in the loop to append the min or max values.
        for parameter in list(parameters_dict.keys()):
            reference_point.loc[(reference_point.Vehicle == str(vehicle)), parameter] = parameters_dict[parameter]

        # Calculates 'TPS_learn_Status': (Learn_TPS2 manually stored in 'Learn_TPS.xlsx' - Learn_TPS2 recorded from data).
        os.chdir(main_wd) # changes the cwd to the main_wd
        Learn_TPS = pd.read_excel("Learn_TPS.xlsx")
        
        if len(Learn_TPS['Vehicle'].isin([int(vehicle)]).unique()) == 1:
            print('Learn_TPS values not found for vehicle ' + str(vehicle))
        else:
            for TPS2MinMax in ['Learn_TPS2Min','Learn_TPS2Max']:
                Learn_TPS_Status = (int(Learn_TPS[Learn_TPS['Vehicle'] == int(vehicle)][TPS2MinMax]) 
                                    - int(reference_point[reference_point['Vehicle'] == (vehicle)][TPS2MinMax]))
                # Append 'Learn_TPS_Status' to the reference_point DataFrame
                reference_point.loc[(reference_point.Vehicle == str(vehicle)), (TPS2MinMax + str('_Status'))] = Learn_TPS_Status
                
    return reference_point, average_TPS