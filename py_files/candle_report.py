import glob
import pandas as pd 
import matplotlib.pyplot as plt
import export.config
import seaborn as sns
import os
from matplotlib.cbook import boxplot_stats


def candle_report(excel_report_directory):  
    
    #main_wd = export.config.main_wd
    #os.chdir(main_wd)
    #os.chdir('../')
    
    data = pd.DataFrame()
    
    for file in glob.glob(excel_report_directory):
        data = pd.concat([data,pd.read_excel(file)])
        
    yaxis = export.config.yaxis
    
    fig, axes = plt.subplots(len(yaxis),1, figsize=(10,45))
    sns.set(style="whitegrid")
    session_list = list(data.Session.unique())
    
    i = 0
    for parameter in yaxis:
        axes[i] = sns.boxplot(x='Session', y=parameter, data=data, ax=axes[i], palette="Set2")
              
        # Loop through each session:
        for session in range(0, len(session_list)):   
            data_loop = data  # Restores data  
            # Gets the fliers (outliers of the boxplot) for each session:
            data_loop = data[data['Session'] == session_list[session]]
            fliers = boxplot_stats(data_loop[data_loop['Session'] == session_list[session]][parameter]).pop(0)['fliers']       
            # Loops through each vehicle to find the correspoding outlier
            for vehicle_loop in range(0, len(fliers)):
                # Gets the corresponding vehicle for each outlier
                vehicle = data_loop[data_loop[parameter] == fliers[vehicle_loop]]['Vehicle']
                outlier = list(data_loop[data_loop[parameter] == fliers[vehicle_loop]][parameter])
                axes[i].annotate(('#' + str(list(vehicle))), (session + 0.1, outlier[0]))
    
        i += 1
        
        
    fig.savefig('test.png', dpi=300)   