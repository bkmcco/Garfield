import ROOT
import Garfield
import os
import ctypes
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt
import csv

def write_csv(data, directory, filename):

    #for writing csv w gain measurements
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, filename)
    
    
    with open(file_path, mode = 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

path = os.getenv('GARFIELD_INSTALL')

trials = 1
pressure = 760. * 1.5
file_name = '0_102.csv'
directory = '/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V'


fm = ROOT.Garfield.ComponentAnsys123()
fm.Initialise("ELIST.lis", "NLIST.lis", "MPLIST.lis", "PRNSOL.lis", "micron")
fm.EnableMirrorPeriodicityX()
fm.EnableMirrorPeriodicityY()
fm.PrintRange()


pitch = 0.014   #[cm]

gas = ROOT.Garfield.MediumMagboltz("ar", 98., "ch4", 2.)
gas.SetTemperature(293.15)
gas.SetPressure(pressure)
gas.Initialise(True)


rPenning = 0.51
gas.EnablePenningTransfer()


gas.LoadIonMobility('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/IonMobility_Ar+_Ar.txt')
 
fm.SetGas(gas)
fm.PrintMaterials()


sensor = ROOT.Garfield.Sensor()
sensor.AddComponent(fm)
#restrict sensor area to count electron endpoints at z=0
sensor.SetArea(-2, -2, -1, 2,  2, 1)

aval = ROOT.Garfield.AvalancheMicroscopic(sensor)

drift = ROOT.Garfield.AvalancheMC(sensor)
drift.SetDistanceSteps(2.e-4)

driftView = ROOT.Garfield.ViewDrift()
plotDrift = True
if plotDrift:
  aval.EnablePlotting(driftView)
  drift.EnablePlotting(driftView)

# Count the total number of ions and the back-flowing ions.

ne= ctypes.c_int()
ni = ctypes.c_int()

pos_xy = []
positions = []
ne_list = []
count = 0
for i in range(trials):
  num_e = []
  x0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  y0 = -0.5 * pitch + ROOT.Garfield.RndmUniform() * pitch
  z0 = -0.28
  t0 = 0.
  e0 = 0.07
  aval.AvalancheElectron(x0, y0, z0, t0, e0, 0., 0., 0.)
  aval.GetAvalancheSize(ne, ni)
  print(ne)
  
  for electron in aval.GetElectrons():

    p0 = electron.path[0]
    endPoint = electron.path.back()
    if endPoint.z < -0.1:
      #isolating electrons that have endpoints near the bottom GEM 1 plate
      positions.append((endPoint.x, endPoint.y, endPoint.z, electron.status))
      pos_xy.append((endPoint.x,endPoint.y))


print(len(positions))

#keep track of how electrons are being lost + where     
with open('e_status.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['x', 'y', 'z', 'status'])
    
    writer.writerows(positions)
  


x_coords, y_coords = zip(*pos_xy)
plt.scatter(x_coords,y_coords)
plt.ylim(-0.3,0.3)
plt.xlim(-0.2,0.2)
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.savefig("scatter")



cD = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetArea(-0.2, -0.11, 0.2, 0.3)
meshView.SetCanvas(cD)
meshView.SetComponent(fm)
meshView.SetPlane(0, -1, 0, 0, 0, 0)
meshView.SetFillMesh(True)
meshView.SetColor(0, ROOT.kBlue + 3)        #not working to color in kapton on plot
meshView.SetColor(1, ROOT.kGray)
meshView.EnableAxes()
meshView.SetViewDrift(driftView)
meshView.Plot()
cD.Draw()
cD.Update()
cD.SaveAs("zoom_out.png")


cF = ROOT.TCanvas('cD', '', 600, 600)
meshView = ROOT.Garfield.ViewFEMesh()
meshView.SetArea(-0.02, -0.11, 0.02, -0.098)
meshView.SetCanvas(cF)
meshView.SetComponent(fm)
meshView.SetPlane(0, -1, 0, 0, 0, 0)
meshView.SetFillMesh(True)
meshView.SetColor(0, ROOT.kBlue + 3)        #not working to color in kapton on plot
meshView.SetColor(1, ROOT.kGray)
meshView.EnableAxes()
meshView.SetViewDrift(driftView)
meshView.Plot()
cF.Draw()
cF.Update()
cF.SaveAs("zoom_in.png")


#print(sum(ne_list)/len(ne_list))
#write_csv(ne_list,directory, file_name)
