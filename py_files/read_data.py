
import pandas as pd
import glob
import os

def read_data(target_folder, main_wd, method=pd.read_table):
    """This function searches for all ASCII (.prn) files exported from the Marelli Wintax 4
    to create a 'database'pandas DataFrame which contains data of all cars in a given session. 
    
    Keyword arguments:
    target_folder -- path to the folder containing the .prn files 
    main_wd -- main working directory
    method -- pandas method to read the ASCII files (default=pd.read_table)
    
    There are two ways of exporting data from Marelli: all laps appended and the default method
    which exports each lap in a different file. Appended method runs much faster.
    The .prn files are named by default with the following structure:
    
    - Tr0000_Abs00000000_TeamName_CarNumber_Lap0_cableData (non appended export)
    - Append_Tr0000_Abs00000000_TeamName_CarNumber_Lap0_cableData (appended export)
    
    IMPORTANT: do not change the default file name
    """     
    database = pd.DataFrame()
    os.chdir(str(main_wd) + '\\' + target_folder)

    for file in glob.glob('*.prn'):
        data_temp = method(file, delim_whitespace=True)
        split_filename = file.split('_')
        # Adjust the index according to the export type
        if split_filename[0] == 'Append':
            index = 1
        else: 
            index = 0
        # Creates a new column with the team name
        data_temp['Team'] = split_filename[index + 2]
        data_temp['Vehicle'] = split_filename[index + 3]   
        data_temp['Session'] = target_folder  
        database = database.append(data_temp)  # Appends each file data to a database
        
    return database