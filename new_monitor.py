import csv
import psychopy.monitors.calibTools as T

# Constructs and saves a new monitor to the given pathname based on the
# given photometer data. Photo data file should be in tab delimited form:
# "input level", "grayscale lum", "red gun lum", green gun lum", "blue gun lum"

# Note: When you want to access a monitor saved into a custom path, must
# change the monitorFolder variable inside of the calibTools module, then 
# get the monitor using <module>.Monitor(monitorName)

# Set runtime parameters for monitor:
path = './calibration/'     # where monitors will be stored


monitors = {
'NNL':#Information for the NNL goggles: 
dict(monitor_name = 'NNL', # name of the new monitor
     calib_file = './calibration/NNLGamma_111409_average.txt', # photometer data
     width = 76.2, # width of the screen (cm)
     distance = 120, # (virtural) distance from the screen (cm)
     size = [800, 600], # size of the screen (px)
     # We can also save notes to our monitor:
     notes = """ The NNL MR-safegoggles with calibration""")
}

# Make sure to change monitorFolder in this module for custom save location
T.monitorFolder = path

for m in monitors.keys():
    monitor = monitors[m]
    # Initialize our intermediary variables and open the text file
    fileobj = open(monitor['calib_file'], 'rU') 
    csv_read = csv.reader(fileobj, dialect=csv.excel_tab)
    input_levels = [];
    lums = {
        'gray' : [],
        'R' : [],
        'G' : [],
        'B' : [] } 
    gamma_vals = lums.copy()
    # Read input levels and luminescence values from file
    for row in csv_read:
        input_levels.append(float(row[0]))
        lums['gray'].append(float(row[1]))
        lums['R'].append(float(row[2]))
        lums['G'].append(float(row[3]))
        lums['B'].append(float(row[4]))

    # Calculate the gamma grid based on given lums
    gammaGrid = []
    for val in lums.keys():
        calculator = T.GammaCalculator(inputs = input_levels, lums = lums[val])
        gamma_vals[val] = [calculator.gammaModel[0], 
            calculator.gammaModel[1], calculator.gammaModel[2]]
        gammaGrid.append(gamma_vals[val])
    # We are not interested in the grayscale value
    del gammaGrid[0]

    # Create the new monitor, set values and save
    newMon = T.Monitor(monitor['monitor_name'],
                       monitor['width'],
                       monitor['distance'])
    newMon.setSizePix(monitor['size'])
    newMon.setNotes(monitor['notes'])
    newMon.setGammaGrid(gammaGrid)
    newMon.setCalibDate()
    newMon.saveMon()
