import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv


'''
This code counts the number of electrons at the inner diameter of GEM hole 1

'''

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
pressure = 760. * 1
file_name = 'in_dens.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/'


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
rPenning = 0.25
gas.EnablePenningTransfer()
# Load the ion mobilities.
gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()

# Assemble the sensor.
sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
sensor.SetArea(-2, -1, -1, 2,  1, -0.101)

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
  x0 = 0
  y0 = 0
  z0 = -0.28
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  aval.GetAvalancheSize(ne, ni)
  ne_list.append(ne.value)


print(sum(ne_list) / len(ne_list))
'''
print(ne_list)
cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetArea(-0.1, -0.11, 0.1, -0.08)
meshView.SetCanvas(cD)
meshView.SetComponent(fm)
# x-z projection.
meshView.SetPlane(-1, 0, 0, 0, 0, 0)
meshView.SetFillMesh(True)
#  Set the color of the kapton.
meshView.SetColor(2, ROOT.kYellow + 3)
meshView.EnableAxes()
meshView.SetViewDrift(driftView)
meshView.Plot()
cD.Draw()
cD.Update()
cD.SaveAs("bottom_gem_1.png")
'''
#write_csv(ne_list,directory, file_name)


'''
  for electron in aval.GetElectrons():
    p0 = electron.path[0]
    drift.DriftIon(p0.x, p0.y, p0.z, p0.t)
    nTotal += 1
    endpoint = drift.GetIons().front().path.back()
    if endpoint.z > 0.005: nBF += 1
'''