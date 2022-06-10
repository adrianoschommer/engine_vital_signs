def filter_data(data, threshold, vehicle):
    """This function filters raw data imported from the Marelli Wintax 4 acording to the given thresholds.
    
    Keyword arguments:
    data -- pd.DataFrame output from the read_data() function 
    threshold -- dictionary of the thresholds to filter data {'Channel_Name':(min threshold,max_threshold), ...}
    
    To avoid raising an error when there is a faulty data, the algorithm searches for a local minimum and maximum 
    when the default thresholds cannot be not met. Then, it prints out the new threshold applied.
    """    
    threshold_list = list(threshold.keys())
    
    for parameter in threshold_list:
                    
        if (max(data[parameter]) > threshold[parameter][0]) & (min(data[parameter]) < threshold[parameter][1]):
            data = data[(data[parameter] > threshold[parameter][0]) & (data[parameter] < threshold[parameter][1])]   
          
        else:
            data = data[(data[parameter] > max(data[parameter])*0.95)]
            print('#' + str(vehicle) + ' [NOK] ' + parameter + ' max = ' + str(max(data[parameter]))
                 + ' | threshold of ' + str(max(data[parameter])*0.95) + ' applied')
            
        if len(data) == 0:
            print('#' + str(vehicle) + ' [NOK] ')
                        
    if len(data) > 0:
        print('#' + str(vehicle) + ' [OK] ' + '(' + str(len(data)) + ')')

    return data