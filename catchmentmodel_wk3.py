# catchmentmodel_wk3.py
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir('C:/Users/ouce/Work/teaching/Oxford_Geog/FHS/DigitalMethodologies/code')
import custom_polygon as pg
import scipy.interpolate


### Some useful numbers
seconds_in_day=60*60*24
sand_density  = 1500      # kg/m^3
### The core model function
def total_sediment_export(Annual_precip, Potential_ET, Catchment_area, 
                          sediment_fraction, channel_width, channel_depth, \
                          Headwaters_altitude, River_length,\
                          aridity_matters=True):
    aridity_index = Annual_precip/float(Potential_ET)
    Annual_precip_m = Annual_precip/1e3 # Convert from mm to metres
    Total_annual_precip = Annual_precip_m * Catchment_area
    Total_annual_discharge = Total_annual_precip*aridity_index
    ### This option specifies that denudation has a dependency on aridity
    ### Why might this dependency exist?
    if aridity_matters: sediment_fraction = 0.5*(1-aridity_index)
    
    Annual_sediment_export = Total_annual_discharge*sediment_fraction
    Sediment_export_tons = Annual_sediment_export/sand_density/1000.
    Annual_discharge_sverdrup = Total_annual_discharge/1e6
    return Sediment_export_tons, Annual_discharge_sverdrup

######### WENT INTO THE FIELD AND MEASURED OUT THE SUBCATCHMENT PROPERTIES ###
catchment_properties = {1:
    {'Annual_precip'  : 700,       # mm/yr
    'Potential_ET' : 2100,        # mm/yr
    'Catchment_area' : 0.5*1e12,  # m^2 (1e6 is computer code for 10^6)
    'Headwaters_altitude' : 4000.,# m
    'River_length' : 500.*1e3,   # m
    'Bedform' : 'sand',           # bedrock, silt-clay, sand, gravel, boulder
    'Channel_depth' : 2,          # m
    'Channel_width' : 5,         # m
    'Sediment_fraction' : 0.2},   # fraction of discharge
     2:
    {'Annual_precip'  : 200,       # mm/yr
    'Potential_ET' : 2000,        # mm/yr
    'Catchment_area' : 0.5*1e12,  # m^2 (1e6 is computer code for 10^6)
    'Headwaters_altitude' : 1000.,# m
    'River_length' : 500.*1e3,   # m
    'Bedform' : 'rock',           # bedrock, silt-clay, sand, gravel, boulder
    'Channel_depth' : 1,          # m
    'Channel_width' : 8,         # m
    'Sediment_fraction' : 0.7},    # fraction of discharge
     3:
    {'Annual_precip'  : 200,       # mm/yr
    'Potential_ET' : 2100,        # mm/yr
    'Catchment_area' : 0.5*1e12,  # m^2 (1e6 is computer code for 10^6)
    'Headwaters_altitude' : 500.,# m
    'River_length' : 500.*1e3,   # m
    'Bedform' : 'rock',           # bedrock, silt-clay, sand, gravel, boulder
    'Channel_depth' : 1,          # m
    'Channel_width' : 8,         # m
    'Sediment_fraction' : 0.7}    # fraction of discharge
}


continent_box = np.zeros((1000,1000))
x,y=np.arange(0,1000), np.arange(0,1000)
### TO MANUAL DEFINE EACH CATCHMENT BOUNDARY THIS BIT OF CODE
### FOLLOWING INSTRUCTIONS CAREFULLY
basinkeys = catchment_properties.keys()
basins=continent_box.copy()
for key in basinkeys:
    plt.figure()
    plt.contourf(basins)
    plt.show()
    print('River basin:',key)
    exec('catchment_poly'+str(key)+' = pg.SelectFromArray(plt.gca(),x,y)')
    print("Select catchment area by creating a polygon.")
    print("Press the 'esc' key to start a new polygon.")

### You must run the above block of code before running this loop below!!
for key in basinkeys:
    exec('data = catchment_poly'+str(key)+'.poly_mask.copy()')
    catchment_properties[key]['area_mask']=data
    basins = np.where(data,basins,key)
plt.figure()
plt.contourf(basins)
### Now that we have basins define, compute Catchment_area parameter
for key in basinkeys:
    area_mask = catchment_properties[key]['area_mask']
    pixels = np.sum(~area_mask)
    ### each pixel is 1km x 1km, so that gives 10^6 m^2
    catchment_properties[key]['Catchment_area'] = pixels*1e6

### Define climatological rainfall pattern
low2high = np.linspace(0,2000,1000)
low2high = np.tile(low2high[:,np.newaxis],(1,1000))

east2west = np.sin(np.linspace(0,2,1000))
east2west = np.tile(east2west[np.newaxis,:],(1000,1))

clim_rainfall = low2high*east2west
plt.figure()
plt.contourf(clim_rainfall);plt.colorbar()

### Compute climatological yield
Total_sediment=0
for key in basinkeys:
    ### First compute area rainfall for each sub-catchment.
    params=catchment_properties[key]
    area_mask = params['area_mask']
    masked_rainfall = np.ma.MaskedArray(clim_rainfall,mask = area_mask)
    area_average_rain = masked_rainfall.mean()
    for prm in params.keys():
        exec("%s = params['%s']" %(prm,prm))
    Sediment,Discharge = total_sediment_export(area_average_rain,Potential_ET,\
                      Catchment_area, Sediment_fraction, Channel_width,\
                      Channel_depth, Headwaters_altitude, River_length)
    Total_sediment += Sediment

print('Annual Mean Sediment Yield for Drainage Basin: %2.2f tons'\
      %(Total_sediment))


### Random rainfall distribution example
x, y, z = 2*np.random.random((3,10))
# Set up a regular grid of interpolation points
xi,yi = np.linspace(x.min(), x.max(), 1000), np.linspace(y.min(), y.max(), 1000)
xi, yi = np.meshgrid(xi, yi)
rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
rainfall_variation = rbf(xi, yi)

### Incorporate random rainfall into for loop to generate interannual
### variability time series
years100_sediment=[]
for yr in range(100):
    x, y, z = 2*np.random.random((3,10))
    # Set up a regular grid of interpolation points
    xi,yi = np.linspace(x.min(),x.max(),1000),np.linspace(y.min(),y.max(),1000)
    xi, yi = np.meshgrid(xi, yi)
    rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
    rainfall_variation = rbf(xi, yi)
    year_rain = rainfall_variation*clim_rainfall
    Total_sediment=0
    for key in basinkeys:
        ### First compute area rainfall for each sub-catchment.
        params=catchment_properties[key]
        area_mask = params['area_mask']
        masked_rainfall = np.ma.MaskedArray(year_rain,mask = area_mask)
        area_avg_rain = masked_rainfall.mean()
        for prm in params.keys():
            exec("%s = params['%s']" %(prm,prm))
        Sediment,Discharge = total_sediment_export(area_avg_rain,Potential_ET,\
                          Catchment_area, Sediment_fraction, Channel_width,\
                          Channel_depth, Headwaters_altitude, River_length)
        Total_sediment += Sediment
    years100_sediment.append(Total_sediment)
plt.figure();plt.plot(years100_sediment)

