import pandas as pd
import numpy as np
#from read_data import read_data
import os
#from filter_data import filter_data
main_wd = os.getcwd()

# thresholds for the average_TPS
max_TPS = 70
min_Pdl = 90
min_VehicleSpeed = 100

# thresholds for the reference point
thld_1_Gear_Pot = (5,7)
thld_1_TPS = 0.03
thld_1_Pdl = (97,105)
thld_1_RPM = (5300,5400)

# thresholds for the min / max values
thld_2_Gear_Pot = (1,7)
thld_2_TPS = 0.03
thld_2_max_TPS = 102
thld_2_Pdl = (97,105)
thld_2_RPM = (3000,5400)


# columns for the excel report
columns = ['Team', 
           'Vehicle', 
           'Session',
           'T_Air',
           'T_Water', 
           'T_Oil',
           'P_Oil',
           'T_Fuel',
           'P_Fuel', 
           'Lambda', 
#               'Lambda2', 
           'GainLoop',
           'Vbatt',
           'Pdl',
           'TPS',  
           'RPM', 
           'Time', 
           'Min_P_Oil',
           'Max_T_Water', 
           'Max_T_Oil', 
           'Min_P_Fuel', 
           'Max_VehicleSpeed',
           'P2P_Available', 
           'Max_TPS', 
           'Learn_TPS2Min', 
           'Learn_TPS2Min_Status', 
           'Learn_TPS2Max', 
           'Learn_TPS2Max_Status']
#               'Advance']


# candle report

excel_report_directory = 'reference_point*'

yaxis = ['T_Water', 
         'T_Oil',
         'P_Oil',
         'T_Fuel',
         'P_Fuel', 
         'Lambda', 
         'GainLoop',
         'Vbatt',
         'Pdl',
         'Learn_TPS2Max_Status',
         'Learn_TPS2Min_Status']
    

