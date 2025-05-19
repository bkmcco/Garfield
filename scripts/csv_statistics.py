import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_statistics(file_path):
    # Read the CSV file
    try:
        df = pd.read_csv(file_path, header=None)
    except Exception as e:
        return f"Error reading the file: {e}"
    
    # Check for numeric columns
    numeric_cols = df.select_dtypes(include='number')
    
    if numeric_cols.empty:
        return "No numeric columns found in the file."

    data = df[0].to_numpy()
    mean = np.mean(data)
    trials = len(data)
    uncertainty = np.std(data)/np.sqrt(trials)



    return mean, uncertainty, trials

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

mean1, unc1, tr1 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_106.csv')
mean2, unc2, tr2 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_1055.csv')
mean3, unc3, tr3 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_105.csv')
mean4, unc4, tr4 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_1045.csv')
mean5, unc5, tr5 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_104.csv')
mean6, unc6, tr6 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_1035.csv')
mean7, unc7, tr7 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_103.csv')
mean8, unc8, tr8 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_1025.csv')
mean9, unc9, tr9 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_102.csv')
mean10, unc10, tr10 = calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/volt/500V/0_1015.csv')

compmean,compunc,comptr =  calculate_statistics('/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/standard/1_5atm.csv')
print(compmean)

z = np.array([-0.106, -0.1055, -0.105, -0.1045, -0.104, -0.1035, -0.103, -0.1025,-0.102,-0.1015])
avg = np.array([mean1, mean2, mean3, mean4, mean5,mean6,mean7,mean8,mean9,mean10])
unc = np.array([unc1,unc2,unc3,unc4,unc5,unc6,unc7,unc8,unc9,unc10])
plt.errorbar(z,avg,yerr=unc)
#plt.gca().invert_xaxis()
plt.xlabel('Z-Location (cm)')
plt.ylabel('# electrons')
plt.savefig('zoom_500')

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
