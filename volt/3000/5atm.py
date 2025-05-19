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

trials = 100
pressure = 760. * 5.5
file_name = '5_5atm.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/3000'


# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("ELIST.lis", "NLIST.lis", "MPLIST.lis", "PRNSOL.lis", "micron")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()
fm.PrintRange()

# Dimensions of the GEM [cm]
pitch = 0.014
'''
fieldView = ROOT.Garfield.ViewField()
cF = ROOT.TCanvas('cF', '', 600, 600)
fieldView.SetCanvas(cF)
fieldView.SetComponent(fm)
# Set the viewing plane (xz plane).
fieldView.SetPlaneXZ()
# Set the plot limits in the current viewing plane.
fieldView.SetArea(-1, -0.5, 1, 0.5)
fieldView.SetVoltageRange(-3200., 0000.)

cF.SetLeftMargin(0.16)
fieldView.Plot("v", "colz")
cF.Update()
cF.Draw()
cF.SaveAs("v.png")

input("press enter")
'''

# Setup the gas.
gas = ROOT.Garfield.MediumMagboltz("ar", 98., "ch4", 2.)
gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.Initialise(True)

# Set the Penning transfer efficiency.
rPenning = 0.51
gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -1, 2,  1, 1)

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
nBF = 0
ne= ctypes.c_int()
ni= ctypes.c_int()

ne_list=[]
for i in range(trials):
  # print i, '/', nEvents
  # Randomize the initial position. 
  x0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  y0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  z0 = -0.28
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  aval.GetAvalancheSize(ne, ni)
  ne_list.append(ne.value)

print(sum(ne_list)/len(ne_list))
write_csv(ne_list,directory, file_name)


'''
  for electron in aval.GetElectrons():
    p0 = electron.path[0]
    drift.DriftIon(p0.x, p0.y, p0.z, p0.t)
    nTotal += 1
    endpoint = drift.GetIons().front().path.back()
    if endpoint.z > 0.005: nBF += 1
'''