import lmdb
import os
import shutil
import multiprocessing
from bitcoin import privtopub, pubtoaddr

# Function to generate keys and addresses for a specific range
def generate_key_range(start_range, end_range, db_path, local_save_path, size_threshold_mb):
    # Open LMDB database
    env = lmdb.open(db_path, map_size=10**9)  # Adjust map_size based on expected DB size
    generated_size = 0
    with env.begin(write=True) as txn:
        for private_key in range(start_range, end_range + 1):
            # Convert private key to public key (CPU)
            public_key = privtopub(private_key)
            
            # Convert public key to Bitcoin address (P2PKH) (CPU)
            address = pubtoaddr(public_key)
            
            # Save key and address to LMDB database
            txn.put(str(private_key).encode(), address.encode())
            
            # Track generated file size
            generated_size += len(str(private_key)) + len(address)
            
            # Print progress
            print(f"Generated key {private_key}, address {address}")
            
            # If generated files exceed threshold, save to local and reset the counter
            if generated_size >= size_threshold_mb * (1024 ** 2):  # Convert MB to bytes
                # Save a copy to the local path
                save_to_local(db_path, local_save_path)
                generated_size = 0  # Reset size tracker

# Function to save the LMDB data to local path when threshold is met
def save_to_local(db_path, local_save_path):
    # Copy the LMDB files to the local folder
    lmdb_files = os.listdir(db_path)
    for file in lmdb_files:
        full_path = os.path.join(db_path, file)
        if os.path.isfile(full_path):
            shutil.copy(full_path, local_save_path)
    print(f"Files saved to {local_save_path}")

# Function to split work across multiple CPU cores
def multiprocess_generate_keys(start_range, end_range, num_processes, db_path, local_save_path, size_threshold_mb=500):
    # Calculate the range each process will handle
    step = (end_range - start_range) // num_processes
    processes = []

    for i in range(num_processes):
        # Define the range for each process
        range_start = start_range + i * step
        range_end = start_range + (i + 1) * step if i < num_processes - 1 else end_range
        
        # Create a new process
        process = multiprocessing.Process(
            target=generate_key_range, 
            args=(range_start, range_end, db_path, local_save_path, size_threshold_mb)
        )
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Ensure all processes finish
    for process in processes:
        process.join()

if __name__ == "__main__":
    # Example arguments for the worker node
    start_range = 0x2000000000000000
    end_range = 0x209b800000000000
    db_path = "/path/to/lmdb/database"
    local_save_path = "/local/directory"

    # Use multiprocessing across CPU cores
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    multiprocess_generate_keys(start_range, end_range, num_processes, db_path, local_save_path)
