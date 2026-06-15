"""
Distributed Monte Carlo Simulation for Area (2D) and Volume (3D) calculations.
This script demonstrates the use of MPI Bcast and Reduce for compute-bound tasks.
"""

# Import the necessary libraries
import os
import numpy as np
from mpi4py import MPI
import math

# Define where our configuration and output files will be saved
FILE_CONFIG = "mc_config.txt"
FILE_OUTPUT = "mc_results_mpi.txt"

def load_or_create_config(filename):
    """
    Reads parameters from a text file. Creates it with defaults if missing.
    """
    # These are our default settings just in case the file doesn't exist yet
    defaults = {
        "total_points": 1000000,
        "dimensions": 2,           
        "radius": 0.5,
        "convergence": 1.0e-6
    }
    
    # If the file is not there, we create it and write the default values inside
    if not os.path.exists(filename):
        print(f"Configuration file '{filename}' not found. Generating default...")
        with open(filename, "w") as f:
            for key, value in defaults.items():
                f.write(f"{key}={value}\n")
        return defaults
    
    # If the file exists, we open it and read it line by line
    config = {}
    with open(filename, "r") as f:
        for line in f:
            # Clean up empty spaces and ignore comments
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=")
                config[key.strip()] = parse_config_value(val)
    # Return the dictionary with all our loaded settings
    return config


def parse_config_value(value):
    """
    If there is a dot, it's a float (decimal), otherwise it's an integer
    """
    value = value.strip()

    try:
        return int(value)
    except ValueError:
        return float(value)

def PI():
    """
    compute PI to be treated as reference for convergence calculation
    """
    # We just grab the true value of Pi from the math library so we can check our error later
    pi = math.pi
    return pi
    
def local_montecarlo(rng, local_points, dimensions):
    """
    The vectorized Monte Carlo engine.
    Generates random coordinates and counts how many fall inside the unit circle/sphere.
    """
    # We process points in batches (chunks) of 100,000. 
    # If we try to do millions at once, we will crash the computer's RAM.
    batch_size = 100000;
    points_inside = 0
    
    # Loop through the total points we need to calculate, jumping by batch_size
    for i in range(0,local_points,batch_size):
        # Make sure the last batch doesn't generate more points than we actually need
        current_batch = min(batch_size,local_points - i)
        
        # Generate random points between 0.0 and 1.0 in a fully vectorized way
        # Shape will be (current_batch, 2) for 2D or (current_batch, 3) for 3D
        coordinates = rng.uniform(0.0, 1.0,(current_batch, dimensions))
    
        # Calculate the squared distance from the center (which is at 0.5, 0.5)
        # Using np.sum along axis 1 sums the row wise means  
        squared_distances = np.sum((coordinates- 0.5)**2, axis=1)
    
        # Count how many points lie inside circle. 
        # The radius is 0.5, so radius squared is 0.25. If distance is <= 0.25, it's inside!
        points_inside += np.sum(squared_distances <= 0.25)
    
    # Return the final count of points that hit the target
    return int(points_inside)

def main():
    # --- MPI INITIALIZATION ---
    # Setup the MPI communicator
    comm = MPI.COMM_WORLD
    # my_rank is the ID of the current core
    my_rank = comm.Get_rank()
    # nproc is the total number of cores working on this job
    nproc = comm.Get_size()
    
    # Setup some initial empty variables
    dimensions = 2
    radius = 0.5
    config = None
    total_points =None

    # --- INPUT HANDLING (Root Only) ---
    # Only the root reads the file.
    if my_rank == 0:
        print(f"--- Monte Carlo Simulation started on {nproc} MPI Processes ---")
        config = load_or_create_config(FILE_CONFIG)
        print(f"Parameters loaded: {config}")
        

    # --- BROADCAST PARAMETERS ---
    # The root sends the config dictionary to all the worker processes so everyone has the rules
    config = comm.bcast(config, root=0)
    
    # Now everyone extracts the variables from the config dictionary
    total_points = int(config["total_points"])
    dimensions = int(config["dimensions"])
    radius = float(config["radius"])
    convergence = float(config["convergence"])
    pi_estimate = 0
    Pi = PI()
    
    # Create a random number generator object.
    # We add my_rank to the seed (42). This guarantees every core generates DIFFERENT random numbers.
    # If we didn't do this, all cores would do the exact same work and parallelization would be useless.
    rng = np.random.default_rng(42+my_rank)
    
    # Start timer. We use a Barrier to make sure all cores wait here and start the clock at the exact same time.
    comm.Barrier()
    start_time = MPI.Wtime()
    
    # Keep running the simulation until the difference between our guess and real Pi is smaller than the desired threshold
    while abs(Pi- pi_estimate)>convergence:
        
        # Calculate how many points this specific process needs to calculate
        local_points = int(total_points/nproc)
        # Find out if there are leftover points that don't divide perfectly by the number of cores
        remainder = total_points % nproc
        
        # If there are leftovers, give one extra point to the first few ranks until the remainder is gone
        if my_rank < remainder:
            local_points = local_points + 1
        else:
            # Original code has this standing alone. It basically does nothing but keeps local_points as is.
            local_points 

        # --- PARALLEL COMPUTATION ---
        # No Scatter needed. Every process just generates its own points natively by calling the montecarlo engine.
        local_inside = local_montecarlo(rng, local_points, dimensions)

        # --- REDUCE (Data Gathering) ---
        # We don't need a huge array back. We just need to SUM all the local_inside integers.
        # We must put our numbers into numpy arrays because uppercase MPI commands (Reduce) require it.
        send_buf = np.array(local_inside, dtype=np.int64)
        recv_buf = np.array(0, dtype=np.int64)

        # All processes send their single integer, and the root receives the mathematical SUM of all of them
        comm.Reduce(send_buf, recv_buf, op=MPI.SUM, root=0)

        
        if my_rank == 0:
            # The root grabs the final summed value from the receive buffer
            global_inside = recv_buf.item()
        
            # Calculate Pi based on dimensions
            if dimensions == 2:
                # Circle: Area of square is 1. Area of circle is Pi/4. 
                # So we multiply the ratio by 4 to get our Pi estimate.
                pi_estimate = 4.0 * (global_inside / total_points)
                result_val = pi_estimate * (radius**2)
                metric_name = "Area"
                difference = abs(pi_estimate - Pi)
                # print(f"The difference is : {difference}")
                
                # If the guess is still bad, we increase the number of points and try again
                if abs(Pi- pi_estimate)> convergence:
                    total_points = total_points + 10000
                
            
            elif dimensions == 3:
                # Sphere: Volume of cube is 1. Volume of sphere is Pi/6. 
                # So we multiply the ratio by 6 to get our Pi estimate.
                pi_estimate = 6.0 * (global_inside / total_points)
                result_val = (4.0 / 3.0) * pi_estimate * (radius**3)
                metric_name = "Volume"
                difference = abs(pi_estimate - Pi)
                # print(f"The difference is : {difference}")
        
                if abs(Pi- pi_estimate)> convergence:
                    total_points = total_points + 10000
                    

        # The root broadcasts the new pi_estimate and total_points to everyone.
        # This way, all the workers know if they should break the while loop, or if they have to run it again with the new total_points.
        pi_estimate = comm.bcast(pi_estimate, root=0)
        total_points = comm.bcast(total_points, root=0)
        
    # We exit the while loop once the math converges. Wait for everyone to finish, then stop the clock.
    comm.Barrier()
    end_time = MPI.Wtime()
    
    # Only the root prints the final results and writes the file
    if my_rank ==0:
        
        execution_time = end_time - start_time
        # Print results to the terminal
        print("\n--- SIMULATION RESULTS ---")
        print(f"Estimated Pi value : {pi_estimate:.14f}")
        print(f"Calculated {metric_name}  : {result_val:.8f}")
        print(f"MPI Execution Time : {execution_time:.4f} seconds")
        print(f"MPI total points that leads to convergence:{total_points}")

        # Save all the final data into our text report
        with open(FILE_OUTPUT, "a") as f:
            f.write("--- MONTE CARLO HPC REPORT ---\n")
            f.write(f"MPI Processes : {nproc}\n")
            f.write(f"Total Points  : {total_points}\n")
            f.write(f"Dimensions    : {dimensions}D\n")
            f.write(f"Radius        : {radius}\n")
            f.write(f"Pi Estimate   : {pi_estimate:.14f}\n")
            f.write(f"Final {metric_name}    : {result_val:.8f}\n")
            f.write(f"Compute Time  : {execution_time:.4f} seconds\n")
            
        print(f"Results saved to {FILE_OUTPUT}")

# This tells Python to run the main() function when we start the script
if __name__ == "__main__":
    main()