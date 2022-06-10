
import export
import pandas as pd
import numpy as np

def excel_report(target_folder):
    
    reference_point, average_TPS = export.preprocessing(target_folder)    
    
    # Not all columns of the raw data are going into the final report so we have to list which one are going to be used:
    columns = export.config.columns
    
    writer = pd.ExcelWriter(str('reference_point_TESTE' + str(target_folder.split(sep='/')[1]) + '.xlsx'), engine='xlsxwriter')
    reference_point.to_excel(writer, columns = columns, index = False)
    #reference_point.to_excel(writer)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    
    # Add a format. Red / Green
    format = [workbook.add_format({'bg_color': '#FFC7CE','font_color': '#9C0006'}),
              workbook.add_format({'bg_color': '#C6EFCE','font_color': '#006100'})]
    
# =============================================================================
#     average_TPS = np.average(database[(database['TPS'] < export.config.max_TPS) & 
#                                       (database['Pdl'] > export.config.min_Pdl) & 
#                                       (database['VehicleSpeed'] > export.config.min_VehicleSpeed)]['TPS'])      
#     
# =============================================================================
    
    thresholds = {'T_Water':(50,90),
              'T_Oil':(50,105), 
              'P_Oil':(3,5.5),
              'P_Fuel':(3.1,4), 
              'Lambda':(0.8,0.84),
              'Lambda2':(0.75,0.85), 
              'GainLoop':(0.93,1.07), 
              'Vbatt':(11.5,14), 
              'Pdl':(99,101.5),
              'TPS':(average_TPS*0.98,average_TPS*1.02),
              'Min_P_Oil':(3,5.5), 
              'Max_T_Water':(50,95),
              'Max_T_Oil':(50,110), 
              'Min_P_Fuel':(3.1,4), 
              'P2P_Available':(0.5,50), 
              'Learn_TPS2Min_Status':(-1,1),
              'Learn_TPS2Max_Status':(-1,1)}
    
    i = 0
    for column in columns:
        if column in thresholds:
            worksheet.conditional_format(1,i, len(reference_point),i, {'type': 'cell', 
                                                                       'criteria': 'between',
                                                                       'minimum': thresholds[column][0],
                                                                       'maximum': thresholds[column][1],
                                                                       'format': format[1]})
    
            worksheet.conditional_format(1,i, len(reference_point),i, {'type': 'cell',
                                                                       'criteria': 'not between',
                                                                       'minimum': thresholds[column][0],
                                                                       'maximum': thresholds[column][1],
                                                                       'format': format[0]})         
        else:
            worksheet.conditional_format(1,i, len(reference_point),i, {'type': 'top',
                                                                       'value':  5, 
                                                                       'format': format[0]})
        i += 1
        
    worksheet.autofilter(0,0, len(reference_point),len(columns)-1)
    writer.save()