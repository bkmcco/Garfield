import subprocess


executable1 = "/afs/cern.ch/user/b/bmcconne/private/garfieldpp/GEM/triple_gem/nd-gar/gap/tgap1/cdens.py"


num_runs = 100

def run_python_script(executable, times):
    for i in range(times):
        print(f"Running {executable} - Attempt {i+1}/{times}")
        try:
            result = subprocess.run(["python", executable], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         
            print(f"Output:\n{result.stdout.decode(errors='ignore')}")
        except subprocess.CalledProcessError as e:
          
            print(f"Error while running script: {e.stderr.decode(errors='ignore')}")

run_python_script(executable1, num_runs)