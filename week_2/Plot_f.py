from matplotlib import pyplot as plt

def plot_f(t, h, tm):
    time_axis = t
    hum_axis = h
    temp_axis = tm
    plt.plot(time_axis, hum_axis, temp_axis)
    plt.ylabel('Humidity and Temperature')                                                          
    plt.xlabel('Time')                                                              
    plt.title("Humidity & Temperature Graph")                                                    
    # plt.grid(True)                                                                
    plt.tight_layout()                                                              
    plt.show() 

