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

# Function to assign key ranges to workers
def assign_key_range(worker_id):
    # Assign ranges based on worker_id. Adjust the ranges as necessary.
    if worker_id == "v4u5uew9hcix6u":  # Worker 1
        return 0x2000000000000000, 0x209b800000000000
    elif worker_id == "hy8y0x8icq1jo2":  # Worker 2
        return 0x209b800000000001, 0x2137000000000000
    elif worker_id == "rbusy21pgltamx":  # Worker 3
        return 0x2137000000000001, 0x21d2000000000000
    elif worker_id == "7kx98cbk895yar":  # Worker 4
        return 0x21d2000000000001, 0x2236e00000000000
    elif worker_id == "n1eoc1tzc1cd1u":  # Worker 5
        return 0x2236e00000000001, 0x22d1c80000000000
    elif worker_id == "zrowu8zyj9nyp3":  # Worker 6
        return 0x22d1c80000000001, 0x236cb00000000000
    # Add more workers as needed

# Function to distribute subranges dynamically to workers
def distribute_work(worker_id):
    key_range = assign_key_range(worker_id)
    
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

# Function to check the health of a worker
def check_worker_health(worker_id, job_id):
    """
    Check the health of a worker by calling the health endpoint.
    """
    try:
        response = requests.get(
            f"{HEALTH_ENDPOINT}/{job_id}",
            headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"}
        )
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get('status') == 'healthy':
                logger.info(f"Worker {worker_id} is healthy.")
                send_discord_alert(f"Worker {worker_id} (Job ID: {job_id}) is healthy.")
            else:
                logger.warning(f"Worker {worker_id} is not healthy.")
                send_discord_alert(f"Worker {worker_id} (Job ID: {job_id}) is not healthy.")
        else:
            logger.error(f"Failed to check health for worker {worker_id} (Job ID: {job_id}).")
            send_discord_alert(f"Failed to check health for worker {worker_id} (Job ID: {job_id}). Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error checking health for worker {worker_id} (Job ID: {job_id}): {str(e)}")
        send_discord_alert(f"Error checking health for worker {worker_id} (Job ID: {job_id}): {str(e)}")

# Function to cancel a worker's job if needed
def cancel_worker_job(worker_id, job_id):
    """
    Cancel a worker's job by calling the cancel endpoint.
    """
    try:
        response = requests.post(
            f"{CANCEL_ENDPOINT}/{job_id}",
            headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"}
        )
        if response.status_code == 200:
            logger.info(f"Successfully canceled job for worker {worker_id}.")
            send_discord_alert(f"Successfully canceled job for worker {worker_id} (Job ID: {job_id}).")
        else:
            logger.error(f"Failed to cancel job for worker {worker_id}. Status code: {response.status_code}")
            send_discord_alert(f"Failed to cancel job for worker {worker_id} (Job ID: {job_id}). Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error canceling job for worker {worker_id} (Job ID: {job_id}): {str(e)}")
        send_discord_alert(f"Error canceling job for worker {worker_id} (Job ID: {job_id}): {str(e)}")

# Function to monitor the worker progress
def check_worker_progress(job_ids):
    """
    Check the progress of each assigned subrange by calling the serverless endpoint.
    
    Args:
        job_ids (Dict[str, str]): A dictionary mapping worker IDs to their corresponding job IDs.
    """
    for worker_id, job_id in job_ids.items():
        try:
            response = requests.get(
                f"{STATUS_ENDPOINT}/{job_id}",
                headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"}
            )
            
            if response.status_code == 200:
                status_data = response.json()
                status = status_data.get('status')
                
                if status == 'COMPLETED':
                    send_discord_alert(f"Worker {worker_id} (Job ID: {job_id}) has completed processing.")
                elif status == 'IN_PROGRESS':
                    progress = status_data.get('progress', {})
                    current_position = int(progress.get('current_position', '0'), 16)
                    keys_generated = progress.get('keys_generated', 0)
                    addresses_generated = progress.get('addresses_generated', 0)
                    
                    # Calculate overall progress
                    overall_progress = (keys_generated + addresses_generated) / 2
                    
                    send_discord_alert(f"Worker {worker_id} (Job ID: {job_id}) progress:\n"
                                       f"Current Position: {hex(current_position)}\n"
                                       f"Keys Generated: {keys_generated}\n"
                                       f"Addresses Generated: {addresses_generated}\n"
                                       f"Overall Progress: {overall_progress:.2f}%")
                else:
                    send_discord_alert(f"Worker {worker_id} (Job ID: {job_id}) status: {status}")
            else:
                send_discord_alert(f"Failed to get status for worker {worker_id} (Job ID: {job_id}). Status code: {response.status_code}")
        except Exception as e:
            send_discord_alert(f"Error checking progress for worker {worker_id} (Job ID: {job_id}): {str(e)}")

# You can then call these functions in your main loop
if __name__ == "__main__":
    # Define job_ids dictionary
    worker_ids = [
        "6trkpi9vzk6sg0", "v4u5uew9hcix6u", "hy8y0x8ic1j0z",
        "rbusy21pgltamx", "7kx98cbk895yar", "n1eoc1tzc1cd1u"
    ]
    job_ids = {}
    
    # Distribute work and populate job_ids
    for worker_id in worker_ids:
        job_id = distribute_work(worker_id)
        job_ids[worker_id] = job_id

    # Continuously monitor worker progress
    while True:
        try:
            check_worker_progress(job_ids)

            # Check health of all workers periodically
            for worker_id, job_id in job_ids.items():
                check_worker_health(worker_id, job_id)

            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            send_discord_alert(f"Error in monitoring loop: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying if there's an error
