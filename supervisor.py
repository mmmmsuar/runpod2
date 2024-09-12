# supervisor.py

import requests
import time
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
RUN_ENDPOINT = os.getenv('RUN_ENDPOINT')
STATUS_ENDPOINT = os.getenv('STATUS_ENDPOINT')
CANCEL_ENDPOINT = os.getenv('CANCEL_ENDPOINT')
HEALTH_ENDPOINT = os.getenv('HEALTH_ENDPOINT')
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')

# Function to send a Discord alert
def send_discord_alert(message):
    data = {
        "content": message,
        "username": "BTC Puzzle Supervisor"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# Function to assign key ranges dynamically based on the worker index
def assign_key_range(worker_index, total_workers):
    # Full key range: 20000000000000000 to 3ffffffffffffffff
    try:
        full_range_start = 0x20000000000000000
        full_range_end = 0x3ffffffffffffffff
        
        total_range_size = full_range_end - full_range_start
        range_size_per_worker = total_range_size // total_workers
        
        worker_start = full_range_start + (worker_index * range_size_per_worker)
        worker_end = worker_start + range_size_per_worker - 1 if worker_index < total_workers - 1 else full_range_end
        
        logger.info(f"Worker {worker_index} assigned range {hex(worker_start)} to {hex(worker_end)}")
        return worker_start, worker_end
    except Exception as e:
        logger.error(f"Error in assign_key_range for worker {worker_index}: {str(e)}")
        send_discord_alert(f"Error in assign_key_range for worker {worker_index}: {str(e)}")
        return None

# Function to distribute subranges dynamically to workers
def distribute_work(worker_id, worker_index, total_workers):
    key_range = assign_key_range(worker_index, total_workers)
    
    if key_range is None:
        logger.error(f"Key range for worker {worker_id} (worker index {worker_index}) is None.")
        send_discord_alert(f"Failed to assign a key range for worker {worker_id}.")
        return None

    # Prepare input for RunPod workers
    input_data = {
        "input": {
            "start_range": hex(key_range[0]),
            "end_range": hex(key_range[1]),
            "db_path": "/tmp/lmdb_database",  # Path used by worker to store data
            "local_save_path": "/tmp/local_save",  # Local save path for each worker
            "script_url": "https://github.com/yourusername/yourrepo/worker.py"
        }
    }
    
    # Call the RunPod serverless function
    try:
        response = requests.post(
            RUN_ENDPOINT,
            headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
            json=input_data
        )
        
        if response.status_code == 200:
            job_id = response.json().get('id')
            logger.info(f"Worker {worker_id} started with job ID: {job_id}")
            send_discord_alert(f"Worker {worker_id} started processing range {hex(key_range[0])} to {hex(key_range[1])}")
            return job_id
        else:
            logger.error(f"Failed to start worker {worker_id}. Status code: {response.status_code}")
            send_discord_alert(f"Failed to start worker {worker_id} for range {hex(key_range[0])} to {hex(key_range[1])}")
            return None
    except Exception as e:
        logger.error(f"Error in distributing work for worker {worker_id}: {str(e)}")
        send_discord_alert(f"Error in distributing work for worker {worker_id}: {str(e)}")
        return None

# You can then call these functions in your main loop
if __name__ == "__main__":
    # Manually define worker IDs
    worker_ids = [
        "v4u5uew9hcix6u", "hy8y0x8ic1j0z", "rbusy21pgltamx", 
        "7kx98cbk895yar", "n1eoc1tzc1cd1u", "zrowu8zyj9nyp3"
    ]
    
    job_ids = {}
    total_workers = len(worker_ids)

    # Distribute work and populate job_ids
    for worker_index, worker_id in enumerate(worker_ids):
        job_id = distribute_work(worker_id, worker_index, total_workers)
        if job_id is not None:
            job_ids[worker_id] = job_id

    # Continuously monitor worker progress and health
    while True:
        try:
            check_worker_progress(job_ids)

            # Check health of all workers periodically
            for worker_id, job_id in job_ids.items():
                check_worker_health(worker_id, job_id)

            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            send_discord_alert(f"Error in monitoring loop: {str(e)}")
            time.sleep(60)
