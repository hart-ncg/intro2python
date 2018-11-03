# climatespiral.py
'''A script based on https://www.dataquest.io/blog/climate-temperature-spirals-python/ example, that generates the famous Ed Hawkins Climate Spiral.'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
#if not os.path.exists('HadCRUT.4.6.0.0.monthly_ns_avg.txt'):
#    urllib.urlretrieve("https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series/HadCRUT.4.6.0.0.monthly_ns_avg.txt","HadCRUT.4.6.0.0.monthly_ns_avg.txt")
#
### FIRST MOVE TO DIRECTORY WHERE THE DATA IS SAVE (edit accord to your download)
os.chdir('C:/Users/ouce/Work/teaching/Oxford_Geog/FHS/DigitalMethodologies/code')

### OPEN THE GLOBAL MEAN TEMPERATURE FILE INTO DATAFRAME hadcrut
hadcrut = pd.read_csv(
    "HadCRUT.4.6.0.0.monthly_ns_avg.txt",
    delim_whitespace=True,
    usecols=[0, 1],
    header=None
)
### LOOK AT FILE TO SEE WHAT YOU HAVE OPENED
hadcrut.head()

### SPLIT FIRST COLUM OF DATA INTO YEAR AND MONTH AND ADD AS COORDINATED
### DESCRIPTORS, year & month, TO DATAFRAME
hadcrut['year'] = hadcrut.iloc[:, 0].apply(lambda x: x.split("/")[0]).astype(int)
hadcrut['month'] = hadcrut.iloc[:, 0].apply(lambda x: x.split("/")[1]).astype(int)
### RENAME SECOND COLUMN (INDEX=1) TO value
hadcrut = hadcrut.rename(columns={1: "value"})
hadcrut = hadcrut.iloc[:, 1:]

### LOOK AT FILE TO SEE CHANGES
hadcrut.head()

### DROP ALL 2018 DATA FROM DATAFRAME (SINCE DON'T HAVE FULL YEAR YET)
hadcrut = hadcrut.drop(hadcrut[hadcrut['year'] == 2018].index)
hadcrut = hadcrut.set_index(['year', 'month'])
### OBTAIN PRE-1900 MEAN TEMPERATURE AND REMOVE FROM DATASET
hadcrut -= hadcrut.loc[1850:1900].mean()
hadcrut = hadcrut.reset_index()

### SET UP FIGURE AXES
fig = plt.figure(figsize=(8,8))
ax1 = plt.subplot(111, projection='polar')
### LETS PLOT DATA FOR 19850 FIRST
hc_1850 = hadcrut[hadcrut['year'] == 1850]
# Now specify radial distance of each point using temperature from months
# of 1850
r = hc_1850['value'] + 1 # Add 1 just to make plot work better
theta = np.linspace(0, 2*np.pi, 12) # Specify angle so that each month
# is plotted 1/12th of the way around the circle, to complete rotation
ax1.plot(theta, r)
### REMOVE AXES TICK LABELS FOR  A BETTER PLOT
ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
### CHANGE COLORS OF THE FACE OF PLOT AND BACKGROUND
fig.set_facecolor("#323331")
ax1.set_facecolor('#000100')
### lETS ADD AXES TITLE
ax1.set_title("Global Temperature Change (1850-2017)", color='white', fontdict={'fontsize': 30})
ax1.text(0,0,"1850", color='white', size=30, ha='center')

### NOW LETS PLOT ALL YEARS
fig = plt.figure(figsize=(14,14))
ax1 = plt.subplot(111, projection='polar')
ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
fig.set_facecolor("#323331")
ax1.set_facecolor('#000100')
ax1.set_ylim(0, 3.25) # broaden axes to ensure all years will fit in plot
theta = np.linspace(0, 2*np.pi, 12)
ax1.set_title("Global Temperature\nChange (1850-2017)",\
              color='white', fontdict={'fontsize': 20})
years = hadcrut['year'].unique() # GET AN ARRAY OF EACH YEAR IN DATAFRAME
### LOOP THROUGH ALL YEARS IN DATAFRAME, PLOT ALL THE MONTHS IN EACH YEAR
for year in years:
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
    #ax1.text(0,0, str(year), color='white', size=30, ha='center')
    ax1.plot(theta, r)

### WHAT A MESS, LETS IMPROVE THIS BY CHANGING LINE COLOR FROM DEFAULT
### TO THE VIRIDIS COLORMAP
fig = plt.figure(figsize=(14,14))
ax1 = plt.subplot(111, projection='polar')
ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
fig.set_facecolor("#323331")
ax1.set_title("Global Temperature Change (1850-2017)",\
                   color='white', fontdict={'fontsize': 20})
ax1.set_facecolor('#000100')
for index, year in enumerate(years):
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
    theta = np.linspace(0, 2*np.pi, 12)
    ax1.grid(False) 
    ax1.set_ylim(0, 3.25)
    # Here is where we specify a better color using a colormap
    ax1.plot(theta, r, c=plt.cm.viridis(index*2))
### NOW TO ADD SOME REFERENCE TEMPERATURES TO AID INTERPRETATION OF FIGURE
full_circle_thetas = np.linspace(0, 2*np.pi, 1000)
blue_line_one_radii = [1.0]*1000
red_line_one_radii = [2.5]*1000
red_line_two_radii = [3.0]*1000

ax1.plot(full_circle_thetas, blue_line_one_radii, c='blue')
ax1.plot(full_circle_thetas, red_line_one_radii, c='red')
ax1.plot(full_circle_thetas, red_line_two_radii, c='red')

ax1.text(np.pi/2,1.0,"0.0C",color="blue",ha='center',fontdict={'fontsize':20}) 
ax1.text(np.pi/2,2.5,"1.5C",color="red",ha='center',fontdict={'fontsize':20})
ax1.text(np.pi/2,3.0,"2.0C",color="red",ha='center',fontdict={'fontsize':20})

# To be able to write out the animation as a GIF file
import sys
from matplotlib.animation import FuncAnimation

# Create the base plot
fig = plt.figure(figsize=(8,8))
ax1 = plt.subplot(111, projection='polar')
full_circle_thetas = np.linspace(0, 2*np.pi, 1000)
blue_line_one_radii = [1.0]*1000
red_line_one_radii = [2.5]*1000
red_line_two_radii = [3.0]*1000

ax1.plot(full_circle_thetas, blue_line_one_radii, c='blue')
ax1.plot(full_circle_thetas, red_line_one_radii, c='red')
ax1.plot(full_circle_thetas, red_line_two_radii, c='red')

ax1.text(np.pi/2,1.0,"0.0C",color="blue",ha='center',fontdict={'fontsize':20}) 
ax1.text(np.pi/2,2.5,"1.5C",color="red",ha='center',fontdict={'fontsize':20})
ax1.text(np.pi/2,3.0,"2.0C",color="red",ha='center',fontdict={'fontsize':20})
ax1.grid(False)
ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
fig.set_facecolor("#323331")
ax1.set_facecolor('#000100')

def update(i):
    # Specify how we want the plot to change in each frame.
    # We need to unravel the for loop we had earlier.
    year = years[i]
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
    ax1.plot(theta, r, c=plt.cm.viridis(i*2)) 
    ax1.set_ylim(0, 3.25)
    ax1.set_title("Global Temperature change "+str(year),\
                   color='white', fontdict={'fontsize': 20})
    return ax1

anim = FuncAnimation(fig, update, frames=len(years), interval=50)
anim.save('climate_spiral.html', dpi=120, writer='html', savefig_kwargs={'facecolor': '#323331'})

anim = FuncAnimation(fig, update, frames=len(years), interval=100)
anim.save('climate_spiral_100.html', dpi=120, writer='html', savefig_kwargs={'facecolor': '#323331'})
                                                                         
#anim.save('climate_spiral.gif', dpi=120, writer='imagemagick', savefig_kwargs={'facecolor': '#323331'}) 