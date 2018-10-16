# climatespiral.py
'''A script, based on https://www.dataquest.io/blog/climate-temperature-spirals-python/ example, that generates the famous Ed Hawkins Climate Spiral.'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#if not os.path.exists('HadCRUT.4.6.0.0.monthly_ns_avg.txt'):
#    urllib.urlretrieve("https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series/HadCRUT.4.6.0.0.monthly_ns_avg.txt","HadCRUT.4.6.0.0.monthly_ns_avg.txt")
#
hadcrut = pd.read_csv(
    "HadCRUT.4.6.0.0.monthly_ns_avg.txt",
    delim_whitespace=True,
    usecols=[0, 1],
    header=None
)

hadcrut['year'] = hadcrut.iloc[:, 0].apply(lambda x: x.split("/")[0]).astype(int)
hadcrut['month'] = hadcrut.iloc[:, 0].apply(lambda x: x.split("/")[1]).astype(int)

hadcrut = hadcrut.rename(columns={1: "value"})
hadcrut = hadcrut.iloc[:, 1:]

hadcrut.head()

hadcrut = hadcrut.drop(hadcrut[hadcrut['year'] == 2018].index)
hadcrut = hadcrut.set_index(['year', 'month'])

hadcrut -= hadcrut.loc[1850:1900].mean()
hadcrut = hadcrut.reset_index()
hadcrut.head()

fig = plt.figure(figsize=(8,8))
ax1 = plt.subplot(111, projection='polar')
hadcrut['value'].min()
hc_1850 = hadcrut[hadcrut['year'] == 1850]

fig = plt.figure(figsize=(8,8))
ax1 = plt.subplot(111, projection='polar')

r = hc_1850['value'] + 1
theta = np.linspace(0, 2*np.pi, 12)
ax1.plot(theta, r)
ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])

fig.set_facecolor("#323331")
ax1.set_axis_bgcolor('#000100')

ax1.set_title("Global Temperature Change (1850-2017)", color='white', fontdict={'fontsize': 30})
ax1.text(0,0,"1850", color='white', size=30, ha='center')
hadcrut['value'].max()
ax1.set_ylim(0, 3.25)

fig = plt.figure(figsize=(14,14))
ax1 = plt.subplot(111, projection='polar')

ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
fig.set_facecolor("#323331")
ax1.set_ylim(0, 3.25)

theta = np.linspace(0, 2*np.pi, 12)

ax1.set_title("Global Temperature Change (1850-2017)",\
              color='white', fontdict={'fontsize': 20})
ax1.set_axis_bgcolor('#000100')

years = hadcrut['year'].unique()

for year in years:
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
#     ax1.text(0,0, str(year), color='white', size=30, ha='center')
    ax1.plot(theta, r)


fig = plt.figure(figsize=(14,14))
ax1 = plt.subplot(111, projection='polar')

ax1.axes.get_yaxis().set_ticklabels([])
ax1.axes.get_xaxis().set_ticklabels([])
fig.set_facecolor("#323331")

for index, year in enumerate(years):
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
    theta = np.linspace(0, 2*np.pi, 12)
    
    ax1.grid(False)
    ax1.set_title("Global Temperature Change (1850-2017)",\
                   color='white', fontdict={'fontsize': 20})
    
    ax1.set_ylim(0, 3.25)
    ax1.set_axis_bgcolor('#000100')
#     ax1.text(0,0, str(year), color='white', size=30, ha='center')
    ax1.plot(theta, r, c=plt.cm.viridis(index*2))

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

def update(i):
    # Specify how we want the plot to change in each frame.
    # We need to unravel the for loop we had earlier.
    year = years[i]
    r = hadcrut[hadcrut['year'] == year]['value'] + 1
    ax1.plot(theta, r, c=plt.cm.viridis(i*2))
    return ax1

anim = FuncAnimation(fig, update, frames=len(years), interval=50)

anim.save('climate_spiral.gif', dpi=120, writer='imagemagick', savefig_kwargs={'facecolor': '#323331'}) 
