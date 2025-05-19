import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv


def write_csv(data, directory, filename):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(directory, filename)
    
    # Write the integers to the CSV file
    with open(file_path, mode = 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

path = os.getenv('GARFIELD_INSTALL')

trials = 1
pressure = 760. * 2
#file_name = 'xy_coords.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density'


# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("ELIST.lis", "NLIST.lis", "MPLIST.lis", "PRNSOL.lis", "micron")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()
fm.PrintRange()

# Dimensions of the GEM [cm]
pitch = 0.014

# Setup the gas.
gas = ROOT.Garfield.MediumMagboltz("ar", 90., "co2", 10.)
gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.Initialise(True)

# Set the Penning transfer efficiency.
gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -1, 2,  1, 0.202)

aval = ROOT.Garfield.AvalancheMicroscopic(sensor)

drift = ROOT.Garfield.AvalancheMC(sensor)
drift.SetDistanceSteps(2.e-4)

driftView = ROOT.Garfield.ViewDrift()
plotDrift = True
if plotDrift:
  aval.EnablePlotting(driftView)
  drift.EnablePlotting(driftView)

# Count the total number of ions and the back-flowing ions.
nTotal = 0
ne= ctypes.c_int()
ni= ctypes.c_int()

ne_list=[]

xlist = []
ylist = []
zlist = []



for i in range(trials):
  
  #Define the starting parameters of initial electron
  x0 = 0
  y0 = 0
  z0 = -0.28
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  electrons = aval.GetElectrons()
  print(f"Trial {i}: Number of electrons = {len(electrons)}")
  aval.GetAvalancheSize(ne, ni)
  ne_list.append(ne.value)                         #this gets the total number of electrons that make it to our cutoff

  #Collecting all of the x and y positions of our electrons at the endpoints
  for electron in aval.GetElectrons():
    p0 = electron.path[0]
    endPoint = electron.path.back()
    x_coord = endPoint.x
    y_coord = endPoint.y
    z_coord = endPoint.z
    ylist.append(y_coord)
    xlist.append(x_coord)
    zlist.append(z_coord)

        
    '''        
    for step in electron.path:
        if -0.106 <= step.z <= -0.101:
            xlist.append(step.x)
            ylist.append(step.y)
            zlist.append(step.z)

    '''
file_name = "trajectory_points.csv"
os.makedirs(directory, exist_ok=True)
file_path = os.path.join(directory, file_name)

# Write to CSV
with open(file_path, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["x", "y", "z"])  # Updated header with status column
    for x, y, z, in zip(xlist, ylist, zlist):
        writer.writerow([x, y, z])
    
    
    '''
    p0 = electron.path[0]
    endPoint = electron.path.back()
    x_coord = endPoint.x
    y_coord = endPoint.y

    ylist.append(y_coord)
    xlist.append(x_coord)
    '''

#write_csv(max_dist,directory, file_name)

