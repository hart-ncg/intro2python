# geomorph_toyrivercatchment.py
"""
This python script contains functions and commands that create a toy
model of a river catchment which exports sediments which might contribute to
a sand sea.
"""
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# DEFINITIONS
# ------------------------------------------------------------------------------

### FIRST, WE CAN TAKE THE EQUATIONS PRESENTED IN THE GEOMORPH LECTURES ####
### AND CONVERT THEM INTO COMPUTER CODE FUNCTIONS ##########################


def discharge(w, d, v):
    """
    River discharge based on channel width (w) and depth (d),
    and velocity(v).

    Returns: Discharge in m^3/s
    """
    Q = w * d * v
    return Q


def streamflow_velocity(d, s, bedform="sand"):
    """
    Streamflow based on depth (d), channel gradient (s), and type of bedform,
    computed according to Manning Equation
    Arguments:
    ---------
      "bedrock"
      "silt-clay"
      "sand"
      "gravel"
      "boulder"

    Returns: Velocity in m/s
    """
    manning_coefficient = {
        "bedrock": 0.03,
        "silt-clay": 0.035,
        "sand": 0.03,
        "gravel": 0.045,
        "boulder": 0.05,
    }
    n = manning_coefficient[bedform]
    velocity = (d ** (2 / 3.0) * s ** 0.5) / n
    return velocity


def frac_change_sediment_flux(v1, v2):
    """
    An approximation of change in sediment export based on change in
    flow velocity
    """
    u_star1 = v1 * 0.075  # ~7.5% of v
    u_star2 = v2 * 0.075
    change_in_flux_factor = u_star2 ** 3 / u_star1 ** 3
    return change_in_flux_factor


### Some useful numbers
seconds_in_day = 60 * 60 * 24
sand_density = 1500  # kg/m^3

######### LETS MAKE SOME ASSUMPTIONS FOR A TOY RIVER #########################
# Precip zones for biomes: Arid<200mm, Semi-Arid<800mm, Dry-subhumid>800mm
Annual_precip = 700  # mm/yr
Potential_ET = 2100  # mm/yr
Catchment_area = 0.5 * 1e12  # m^2 (1e6 is computer code for 10^6)
Headwaters_altitude = 4000.0  # m
River_length = 1000.0 * 1e3  # m
Bedform = "sand"  # bedrock, silt-clay, sand, gravel, boulder
Channel_depth = 2  # m
Channel_width = 10  # m
Sediment_fraction = 0.2  # fraction of discharge

### BUILD A TOY MODEL OF SEDIMENT EXPORT BASED ON THIS RIVER AND CATCHMENT ###
def total_sediment_export(
    Annual_precip,
    Potential_ET,
    Catchment_area,
    sediment_fraction,
    channel_width,
    channel_depth,
    Headwaters_altitude,
    River_length,
    variable_denudation=False,
):
    """ function that models the amount of sediment export.
    Arguments:
    ---------
        :Annual_precip (float):
        :Potential_ET (float):
        :Catchment_area (float):
        :sediment_fraction (float):
        :channel_width (float):
        :channel_depth (float):
        :Headwaters_altitude (float):
        :River_length (float):
        :variable_denudation (bool):

    Returns:
    -------
        :Sediment_export_tons (float):
        :Annual_discharge_sverdrup (float):
    """
    aridity_index = Annual_precip / float(Potential_ET)
    Annual_precip_m = Annual_precip / 1e3  # Convert from mm to metres
    Total_annual_precip = Annual_precip_m * Catchment_area
    Total_annual_discharge = Total_annual_precip * aridity_index

    ### This option specifies that denudation has a dependency on aridity
    ###   so as aridity goes up the sediment fraction goes down
    ###   Why might this dependency exist?
    if variable_denudation:
        sediment_fraction = 0.5 * (1 - aridity_index)

    Annual_sediment_export = Total_annual_discharge * sediment_fraction
    Sediment_export_tons = Annual_sediment_export / sand_density / 1000.0
    Annual_discharge_sverdrup = Total_annual_discharge / 1e6

    return Sediment_export_tons, Annual_discharge_sverdrup


# ------------------------------------------------------------------------------
# EXPERIMENTATION
# ------------------------------------------------------------------------------

### WHAT IS THE MOST LIKELY CONTROL ON YEAR TO YEAR VARIATIONS IN TOTAL ######
###################### SEDIMENT EXPORT? ######################################
precipvals = np.arange(100, 2000)
Sediment, Discharge = total_sediment_export(
    precipvals,
    Potential_ET,
    Catchment_area,
    Sediment_fraction,
    Channel_width,
    Channel_depth,
    Headwaters_altitude,
    River_length,
)

### Plot the results
plt.plot(precipvals, Sediment, "r")
plt.ylabel("Sediment Export (tons/yr)", color="r")
plt.xlabel("Annual Precipitation (mm)")
plt.show()

### What happens if denudation rate depends on aridity of the catchment?
### Why might this be true?
precipvals = np.arange(100, 2000)
# Enable denudation rate dependant on aridity with variable_denudation=True
Sediment, Discharge = total_sediment_export(
    precipvals,
    Potential_ET,
    Catchment_area,
    Sediment_fraction,
    Channel_width,
    Channel_depth,
    Headwaters_altitude,
    River_length,
    variable_denudation=True,
)
plt.figure()
plt.plot(precipvals, Sediment, "r")
plt.ylabel("Sediment Export (tons/yr)", color="r")
plt.xlabel("Annual Precipitation (mm)")
plt.twinx()
plt.plot(precipvals, Discharge, "b")
plt.ylabel("River Discharge (10^6 m^3/yr)", color="b")
plt.show()

################ WHAT COULD INDUCE VELOCITY CHANGES? #########################
### Altitude induced changes to gradient?
altitude = np.arange(500, 8000)
Sediment, Discharge = total_sediment_export(
    Annual_precip,
    Potential_ET,
    Catchment_area,
    Sediment_fraction,
    Channel_width,
    Channel_depth,
    altitude[0],
    River_length,
)
gradient = altitude / River_length
streamflow = streamflow_velocity(Channel_depth, gradient, bedform="sand")

plt.figure()
plt.plot(altitude, streamflow, "b")
plt.ylabel("Streamflow Velocity (m/s)", color="b")
plt.xlabel("Altitude (m)")
plt.show()

### Does this velocity change affect potential sediment export?
sedimentchange = frac_change_sediment_flux(streamflow[:-1], streamflow[1:])
# This bit of code fractionally changes sediment export based on increase
# in velocity from previous velocity value, and adds to list of values
sediment_with_alt = [Sediment]
cnt = 1
for delta in sedimentchange:
    sediment_with_alt.append(sediment_with_alt[cnt - 1] * delta)
    cnt += 1

plt.figure()
plt.plot(altitude, sediment_with_alt, "r")
plt.ylabel("Sediment Export (tons/yr)", color="r")
plt.xlabel("Altitude (m)")
plt.show()

######## THE SEDIMENT EXPORT FROM THIS CATCHMENT IS DEPOSITED IN ############
######## A MODERN DAY SAND SEA: GIVEN OUR CONTEMPORARY ESTIMATES ############
######## OF THE DENUDATION RATES, WHAT AGE WOULD YOU ASCRIBE THIS ###########
######## SAND SEA?
Sandsea_area = 35000 * 1e6  # m^2
Averagesand_depth = 5  # m

Sediment, Discharge = total_sediment_export(
    Annual_precip,
    Potential_ET,
    Catchment_area,
    Sediment_fraction,
    Channel_width,
    Channel_depth,
    Headwaters_altitude,
    River_length,
)

age_estimate = Sandsea_area * Averagesand_depth / (Sediment * 1000)
print("Estimated age: %2.0f years" % (int(age_estimate)))

###### COME UP WITH SOME OF YOUR OWN CHANGES TO EXPLORE WAYS IN WHICH #######
########### YOU THINK DENUDATION RATES AND SEDIMENT EXPORTS MAY BE ##########
########### MODIFIED BY EXOGENIC, ENDOGENIC, AND BIOGEOGRAPHICAL ############
########### REGIMES, PROCESSES, AND ECOZONES. ###############################
####
### MAKE A COPY OF THIS SCRIPT AND THEN PLAY WITH THE NUMBERS BASED ON YOUR
### IDEAS. BRING A PPT WITH YOUR FIGURES TO THE TUTORIAL.
