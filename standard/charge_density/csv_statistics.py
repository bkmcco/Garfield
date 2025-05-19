import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_statistics(file_path,column_index):
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f"Error reading the file: {e}"
    
    # Validate column index
    if column_index >= len(df.columns):
        return f"Column index {column_index} out of range."

    # Try to extract the column and convert to numeric
    try:
        data = pd.to_numeric(df.iloc[:, column_index], errors='coerce').dropna()
    except Exception as e:
        return f"Error processing column data: {e}"
    
    if data.empty:
        return "No valid numeric data found in the selected column."

    # Calculate statistics
    mean = np.mean(data)
    trials = len(data)
    uncertainty = np.std(data) / np.sqrt(trials)

    return mean, uncertainty, trials


mean1, unc1, tr1 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_081.csv',1)
mean2, unc2, tr2 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_061.csv',1)
mean3, unc3, tr3 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_041.csv',1)
mean4, unc4, tr4 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_021.csv',1)

print(mean1)

area1, aunc1, atr1 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_081.csv',0)
area2, aunc2, atr2 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_061.csv',0)
area3, aunc3, atr3 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_041.csv',0)
area4, aunc4, atr4 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/charge_density/tgap1/0_021.csv',0)

dist = np.array([-0.081, -0.061, -0.041, -0.021])
cdens = np.array([mean1/area1, mean2/area2, mean3/area3, mean4/area4])
#unc = np.array([unc1,unc2,unc3,unc4,unc5])

#plt.errorbar(pressure, dist, yerr=unc)
plt.plot(dist,cdens)
plt.xlabel('Z-Location [cm]')
plt.ylabel('Charge Density [$1/cm^2$]')
plt.savefig('tgap_cdens')

'''
mean3, unc3, tr3  = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/e_diff/500VG1/arch4982/3.csv')
mean4, unc4, tr4  = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/e_diff/500VG1/arch4982/4.csv')
mean5, unc5, tr5= calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/e_diff/500VG1/arch4982/5.csv')
mean6, unc6, tr6 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/e_diff/500VG1/arch4982/6.csv')
mean7, unc7, tr7= calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/e_diff/500VG1/arch4982/7.csv')

means2, uncs2, trs2= calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/arco29010/2atm.csv')
means3, uncs3, trs3  = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/arco29010/3atm.csv')
means4, uncs4, trs4  = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/arco29010/4atm.csv')
means5, uncs5, trs5= calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/arco29010/5atm.csv')
means6, uncs6, trs6 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/arco29010/6atm.csv')
'''


'''
p1 = np.array([2.0,3.0,4.0,5.0,6.0])
p2 = np.array([3.0,4.0,5.0,6.0,7.0])

avg2 = np.array([mean3,mean4,mean5, mean6, mean7])
unc2 = np.array([unc3,unc4,unc5,unc6,unc7])

avg1 = np.array([means2, means3,means4,means5, means6])
unc1 = np.array([uncs2, uncs3,uncs4,uncs5,uncs6])


plt.errorbar(p2,avg2,yerr=unc2,label='Optimized')
plt.errorbar(p1,avg1,yerr=unc1,label='Standard')


plt.yscale('log')
plt.xlabel('Pressure (atm)')
plt.ylabel('Gain')
plt.legend()

plt.savefig("test")
'''
