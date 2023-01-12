import math 
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
print ("Choose the name of your graph")
fig.suptitle(str(input()))
#----------------------------------------------------------------------------------------------
#This program takes as an imput a .txt file with numerical values 
#And returns the angular speed
#This program is built to function with readData.pl and is originally used for 
#Paper helicopters
#----------------------------------------------------------------------------------------------
SLOPE_SH_HIGH = 8.0
SLOPE_SH_LOW = -8.0

#-------------------------------------
#Requests as an input the file
#to be used by the program
#-------------------------------------

#frequently used /mount/FamilyShare/DataForDad
print ("Write the path and name of the file you want to use as a reference")
file = str(input())

#-------------------------------------------------------------------------
#This function reads a given files and returns the data stored inside"
#-------------------------------------------------------------------------
def Read_File(file_name):
    with open(file_name) as data:
        lines = data.readlines()
        stripped_lines = []
        #Removes \n from the file 
        for i in lines:
            stripped_lines.append (float(i.replace("\n", "") ))
        return stripped_lines

#-------------------------------------------------------------------------
#This function uses the data to find the threshold to mesure the value
#That it will later use to find the rotation.
#-------------------------------------------------------------------------
def Find_Mid(data):
    max = -1e9      #Need to set this to the fist value of the list
    min = 1e9     #Need to set this to the fist value of the list
    for i in data:
        if i<min:
            min = i
        if i>max:
            max = i
    threshold = (max+min)/2
    return threshold


#-------------------------------------------------------------------------
#This function reads the data and returns the time stamps when the 
#Data values go by the threshold and returns two lists: 
# The first one has the timestamps when the data goes up by the threshold
# The seconcd contains the timestamps when the data goes down by the threshold
#-------------------------------------------------------------------------

def Find_threshold_passes(data):

    threshold = Find_Mid(data)
    pass_threshold_up_time = []

    past_i = 9999
    time = 0.0
    last_time = 0
    for i in data:
        if i >= threshold and past_i < threshold and (time-last_time)>0.05:
            pass_threshold_up_time.append(time)
            last_time = time
        past_i = i
        time = time + 0.002
    return pass_threshold_up_time
        
#-------------------------------------------------------------------------
def angular_speed (times_going_up):
    delta_time_up = []
    t_up_past = 0
    for i in times_going_up:
        delta_time_up.append(i-t_up_past)
        t_up_past = i
    #Uncomment print statement for debugging
    #print ("Delta time up",delta_time_up)
    angular_speed_up = []
    for m in delta_time_up:
        if m != 0:
            angular_speed_up.append(math.pi/m)
    
    
    return angular_speed_up


#-------------------------------------------------------------------------

def moving_avg (points_y, points_x):
    point_mov_avg = []
    if len(points_x)>3:
        for i in range (3, len(points_x)):
            avg = sum(points_y[i-3:i])/3
            point_mov_avg.append(avg)
            avg = 0
    
    return point_mov_avg, points_x[1:-2]
    
#-------------------------------------------------------------------------
def slope (points_y, points_x):
    slopes_y = []
    for i in range (len(points_x)-1): 
        dif_y = points_y[i+1]-points_y[i]
        dif_x = points_x[i+1]-points_x[i]
        if dif_x != 0:
            slopes_y.append(dif_y/dif_x)
        else:
            slopes_y.append('nan')
    return slopes_y,points_x[:-1] 

#-------------------------------------------------------------------------

def find_stable(slope_y,slope_x):
    
    stbl_inter = []
    for i in range (len(slope_y)):
        y = slope_y[i]
        if y >= SLOPE_SH_LOW and y <= SLOPE_SH_HIGH:
            stbl_inter.append(slope_x[i])
            break
    for i in range (len(slope_y)):
        y = slope_y[(len(slope_y)-i)-1]
        if i>=SLOPE_SH_LOW and i<=SLOPE_SH_HIGH:
            stbl_inter.append(slope_x[(len(slope_y)-i)-1])
            break
    return stbl_inter
#---------------------------------------------------------------------

def avg (flat,data_y,data_x):
    index_start = data_x.index(flat[0])
    index_end = data_x.index(flat[-1])
    data_x = data_x [index_start:index_end]
    data_y = data_y [index_start:index_end]

    avg = (sum(data_y)/len(data_y))

    return avg
#---------------------------------------------------------------------

def uncert (flat,data_y,data_x,avg):
    index_start = data_x.index(flat[0])
    index_end = data_x.index(flat[-1])
    data_x = data_x [index_start:index_end]
    data_y = data_y [index_start:index_end]

    dif_to_avg = []
    for i in data_y:
        dif_to_avg.append(abs(avg-i))
    return mean(dif_to_avg)




def mean (list):
    return (sum(list)/len(list))            






#print (Find_Mid(Read_File("/mount/FamilyShare/DataForDad/A3.txt")))
#print ("Threshold passes",Find_threshold_passes(Read_File("/mount/FamilyShare/DataForDad/A3.txt")))
up= Find_threshold_passes(Read_File(file))
print(up)

y = angular_speed(up)
print (y)

avg_y, avg_x= moving_avg (y,up)
print (avg_x)

slope_y, slope_x = slope(avg_y,avg_x)
print ("slope", slope_y)

stable_inter = find_stable(slope_y,slope_x)
print ("Interval:",stable_inter)

stable = avg (stable_inter,y,up)
stable_speed = "Vitesse Stable est de environ "+str('{:06.3f}'.format(stable))+"rad/s"
plt.annotate(stable_speed,xy=(stable_inter[0],y[0]))

uncertanty = uncert (stable_inter,y,up,stable)
print (uncertanty)



ax.plot(up,y,marker = ".")
plt.errorbar(up, y, yerr=uncertanty, fmt=".")
#ax.plot(avg_x,avg_y)
#ax.plot(stable_inter,inter_y)
#ax.plot(slope_x,slope_y)
ax.set_xlabel('t(s)')
ax.set_ylabel('Vitesse Angulaire (rad/sec)')
plt.show()