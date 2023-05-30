import sys
import subprocess
import queue
import time
import json
import pickle
import os
from datetime import timedelta

ENV_JSON = 'env.json'
LUMERICAL_EXECUTABLE = json.load(open(ENV_JSON))["LUMERICAL_EXECUTABLE"]
QUEUE_SAVE_PATH = json.load(open(ENV_JSON))["QUEUE_SAVE_PATH"]
        
def save(queue: queue.Queue) -> None:
    serialized_queue = pickle.dumps(queue)
    with open(QUEUE_SAVE_PATH, 'wb') as file:
        file.write(serialized_queue)

def load() -> queue.Queue:
    with open(QUEUE_SAVE_PATH, 'rb') as file:
        serialized_queue = file.read()
    
    return pickle.loads(serialized_queue)

def simulate(simulation_file) -> None:
    start_time = time.monotonic()
    print(f"Started: {simulation_file}")

    subprocess.run([LUMERICAL_EXECUTABLE, "-run", simulation_file])

    end_time = time.monotonic()
    print(
        f"Finished: {simulation_file} \t{timedelta(seconds=(end_time-start_time))}")

def main():
    simulations_queue = 0
    if os.path.exists(QUEUE_SAVE_PATH):
        simulations_queue = load()
    else:
        simulations_queue = queue.Queue()

    for arg in sys.argv[1:]:
        simulations_queue.put(arg)

    save(simulations_queue)
    while not simulations_queue.empty():
        sim = simulations_queue.get()
        simulate(sim)
        save(simulations_queue)

    print(f"Finished all simulations.")

if __name__ == "__main__":
    main()
