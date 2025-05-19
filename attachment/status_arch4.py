import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv

#from spread_analyzer import tuples_to_csv

def tuples_to_csv(data, headers, file_path):
    '''
    Writes list of tuple data to a csv.

    >> data      [list of tuples] : Each tuple is a row of values.
    >> headers   [list of str]    : Column headers titles
    >> file_path [str]            : Path to CSV

    '''
    
    file_exists = os.path.exists(file_path)
    write_header = not file_exists or os.path.getsize(file_path) == 0

    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(headers)
        writer.writerows(data)

'''
This code counts the number of electrons at the upper outer diameter of GEM layer 2

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

trials = 1
pressure = 760. * 1.0
file_name = 'arch4982.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar'


# Load the field map.
fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("ELIST.lis", "NLIST.lis", "MPLIST.lis", "PRNSOL.lis", "micron")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()
fm.PrintRange()

# Dimensions of the GEM [cm]
pitch = 0.014

# Setup the gas.
gas = ROOT.Garfield.MediumMagboltz("ar", 98., "ch4", 2.)
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
sensor.SetArea(-2, -1, -1, 2,  1, 0.25)

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


data = []

status_list = []


for i in range(trials):
  total = 0
  x0 = 0
  y0 = 0
  z0 = -0.15
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  aval.GetAvalancheSize(ne, ni)
  num_endpoints = aval.GetNumberOfElectronEndpoints()

  #counting electron loss points
  attachment_1 = 0            #attachment gap 1
  attachment_2 = 0            #attachment gap 2

  diffusion_1 = 0             #diffusion gap 1
  diffusion_2 = 0             #diffusion gap 2


  for electron in aval.GetElectrons():
    p0 = electron.path[0]
    endPoint = electron.path.back()
    fx = endPoint.x
    fy = endPoint.y
    fz = endPoint.z
    status_code = electron.status
    data.append((fx, fy, fz, status_code))

    if (fz < 0) and (status_code == -7):
      attachment_1 += 1
    
    if (fz > 0) and (status_code == -7):
      attachment_2 += 1

    if (fz < 0) and (status_code == -5):
      diffusion_1 += 1

    if (fz > 0) and (status_code == -5):
      diffusion_2 += 1

  status_list.append((attachment_1, attachment_2, diffusion_1, diffusion_2, num_endpoints))

tuples_to_csv(status_list,['attachment1', 'attachment2', 'diffusion1', 'diffusion2', 'total'], file_name)


'''
area = []

for i in range(len(max_x)):
  r1 = 0.5*(abs(max_x[i])-abs(min_x[i]))
  r2 = 0.5*(abs(max_y[i])-abs(min_y[i]))
  area.append(np.pi*r1*r2)



os.makedirs(directory, exist_ok=True)

# Create the full file path
file_path = os.path.join(directory, file_name)

# Write area and NE to CSV
with open(file_path, mode='a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['area', 'ne'])  # Header
    for a, ne in zip(area, ne_list):
        writer.writerow([a, ne])
'''

'''
cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetArea(-0.05, -0.02, 0.05, 0.02)
meshView.SetCanvas(cD)
meshView.SetComponent(fm)
# x-z projection.
meshView.SetPlane(0, -1, 0, 0, 0, 0)
meshView.SetFillMesh(True)
#  Set the color of the kapton.
meshView.SetColor(2, ROOT.kYellow + 3)
meshView.EnableAxes()
meshView.SetViewDrift(driftView)

meshView.Plot()
cD.Draw()
cD.Update()
cD.SaveAs("debug.png")

#write_csv(ne_list,directory, file_name)
'''

'''
  for electron in aval.GetElectrons():
    p0 = electron.path[0]
    drift.DriftIon(p0.x, p0.y, p0.z, p0.t)
    nTotal += 1
    endpoint = drift.GetIons().front().path.back()
    if endpoint.z > 0.005: nBF += 1
'''