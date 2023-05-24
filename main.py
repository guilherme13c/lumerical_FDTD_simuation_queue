import sys, subprocess, queue, time
from datetime import timedelta

LUMERICAL_EXECUTABLE = ""

def simulate(simulation_file):
    start_time = time.monotonic()
    print(f"Started: {simulation_file}")
    
    subprocess.run([LUMERICAL_EXECUTABLE, "-run", simulation_file])
    
    end_time = time.monotonic()
    print(f"Finished: {simulation_file} \t{timedelta(seconds=(end_time-start_time))}")

simulations_queue = queue.Queue()

for arg in sys.argv[1:]:
    simulations_queue.put(arg)
    
while (not simulations_queue.empty()):
    sim = simulations_queue.get()
    simulate(sim)

print(f"Finished all simulations.")
