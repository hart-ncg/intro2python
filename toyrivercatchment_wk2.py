# geomorph_toyrivercatchment.py
''' 
This python script contains functions and commands that create a toy
model of a river catchment which exports sediments which might contribute to
a sand sea.
'''
import numpy as np
import matplotlib.pyplot as plt

### FIRST, WE CAN TAKE THE EQUATIONS PRESENTED IN THE ESP GEOMORPH LECTURES ###
### AND CONVERT THEM INTO COMPUTER CODE FUNCTIONS #############################

def discharge(w,d,v):
    '''
    River discharge based on channel width (w) and depth (d),
    and velocity(v).

    Returns: Discharge in m^3/s
    '''
    Q = w*d*v
    return Q

def streamflow_velocity(d,s,bedform='sand'):
    '''
    Streamflow based on depth (d), channel gradient (s), and type of bedform,
    computed according to Manning Equation
    bedform can be:
    bedrock
    silt-clay
    sand
    gravel
    boulder
    
    Returns: Velocity in m/s
    '''
    manning_coefficient={'bedrock':0.03,
                        'silt-clay':0.035,
                        'sand':0.03,
                        'gravel':0.045,
                        'boulder':0.05}
    n = manning_coefficient[bedform]
    velocity = (d**(2/3.) * s**0.5) / n 
    return velocity

def frac_change_sediment_flux(v1,v2):
    '''
    An approximation of change in sediment export based on change in
    flow velocity
    '''
    u_star1=v1*.075 # ~7.5% of v
    u_star2=v2*.075
    change_in_flux_factor = u_star2**3/u_star1**3
    return change_in_flux_factor

### Some useful numbers
seconds_in_day=60*60*24
sand_density  = 1500      # kg/m^3

######### LETS MAKE SOME ASSUMPTIONS FOR A TOY RIVER #########################
# Precip zones for biomes: Arid<200mm, Semi-Arid<800mm, Dry-subhumid>800mm
Annual_precip  = 700       # mm/yr
Potential_ET = 2100        # mm/yr
Catchment_area = 0.5*1e12  # m^2 (1e6 is computer code for 10^6)
Headwaters_altitude = 4000.# m
River_length = 1000.*1e3   # m
Bedform = 'sand'           # bedrock, silt-clay, sand, gravel, boulder
Channel_depth = 2          # m
Channel_width = 10         # m
Sediment_fraction = 0.2    # fraction of discharge

### BUILD A TOY MODEL OF SEDIMENT EXPORT BASED ON THIS RIVER AND CATCHMENT ###
def total_sediment_export(Annual_precip, Potential_ET, Catchment_area, 
                          sediment_fraction, channel_width, channel_depth, \
                          Headwaters_altitude, River_length,\
                          aridity_matters=False):
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

### WHAT IS THE MOST LIKELY CONTROL ON  VARIATIONS IN TOTAL SEDIMENT EXPORT?
precipvals = np.arange(100,2000)
Sediment, Discharge = total_sediment_export(precipvals, Potential_ET, \
                      Catchment_area, Sediment_fraction, Channel_width,\
                      Channel_depth, Headwaters_altitude, River_length)
### Plot the results
plt.plot(precipvals,Sediment,'r')
plt.ylabel('Sediment Export (tons/yr)',color='r')
plt.xlabel('Annual Precipitation (mm)')
plt.show()

### What happens if denudation rate depends on aridity of the catchment?
### Why might this be true?
#
# Write your own code
#
#
################ WHAT COULD INDUCE VELOCITY CHANGES? #########################
### Altitude induced changes to gradient?
altitude = np.arange(500,8000)
Sediment, Discharge = total_sediment_export(Annual_precip, Potential_ET, \
                      Catchment_area, Sediment_fraction, Channel_width,\
                      Channel_depth, altitude[0], River_length
gradient = altitude/River_length
streamflow = streamflow_velocity(Channel_depth,gradient,bedform='snd')

plt.figure()
plt.plot(altitude        # incomplete

### Does this velocity change affect potential sediment export?
sedimentchange = frac_change_sediment_flux(streamflow[:-1],streamflow[1:])
# This bit of code fractionally changes sediment export based on increase
# in velocity from previous velocity value, and adds to list of values
sediment_with_alt = [Sediment]
cnt=1
for delta in sedimentchange:
    sediment_with_alt.append(sediment_with_alt[cnt-1]*delta)
    cnt+=1

# Plot this output
# For you to complete

######## THE SEDIMENT EXPORT FROM THIS CATCHMENT IS DEPOSITED IN ############
######## A MODERN DAY SAND SEA: GIVEN OUR CONTEMPORARY ESTIMATES ############
######## OF THE DENUDATION RATES, WHAT AGE WOULD YOU ASCRIBE THIS ###########
######## SAND SEA?
Sandsea_area = 35000*1e6 # m^2
Averagesand_depth = 5    # m

Sediment, Discharge = total_sediment_export(Annual_precip, Potential_ET, \
                      Catchment_area, Sediment_fraction, Channel_width,\
                      Channel_depth, Headwaters_altitude, River_length)
total_volume_sand = ???   # COMPLETE
#
# And write your own code here.
#
print("Estimated age: %2.0f years" %(int(age_estimate)))

###### COME UP WITH SOME OF YOUR OWN CHANGES TO EXPERIMENT USING THIS MODEL