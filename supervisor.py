import requests
import time
import json

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/your_webhook_url' ##UPDATE THIS
RUN_ENDPOINT = 'https://api.runpod.ai/v2/xlo2a7bqkp1fqk/run'
STATUS_ENDPOINT = 'https://api.runpod.ai/v2/xlo2a7bqkp1fqk/status/'
CANCEL_ENDPOINT = 'https://api.runpod.ai/v2/xlo2a7bqkp1fqk/cancel/'
HEALTH_ENDPOINT = 'https://api.runpod.ai/v2/xlo2a7bqkp1fqk/health'

# Function to send a Discord alert
def send_discord_alert(message):
    data = {
        "content": message,
        "username": "Gigi"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# Function to distribute work manually with predefined key ranges
def distribute_work_manual(start_range, end_range):
    task_payload = {
        'start': start_range,
        'end': end_range
    }

    try:
        response = requests.post(RUN_ENDPOINT, json=task_payload)
        if response.status_code == 200:
            task_id = response.json().get('id')
            send_discord_alert(f"Task {task_id} started for range {start_range} to {end_range}")
        else:
            send_discord_alert(f"Error: Failed to start task for range {start_range} to {end_range}")
    except Exception as e:
        send_discord_alert(f"Error: {e}")

if __name__ == "__main__":

     # Step 1: Uncomment the range that needs to be processed and distributed to the workers.

    # Segment 1, Sub-range 1
    distribute_work_manual(0x2000000000000000, 0x209b800000000000)

    # Segment 1, Sub-range 2
    distribute_work_manual(0x209b800000000001, 0x2137000000000000)

    # Segment 1, Sub-range 3
    distribute_work_manual(0x2137000000000001, 0x21d2000000000000)

    # Segment 1, Sub-range 4
    distribute_work_manual(0x21d2000000000001, 0x2236e00000000000)

    # Segment 2, Sub-range 1
    distribute_work_manual(0x2236e00000000001, 0x22d1c80000000000)

    # Segment 2, Sub-range 2
    distribute_work_manual(0x22d1c80000000001, 0x236cb00000000000)

    # Segment 2, Sub-range 3
    distribute_work_manual(0x236cb00000000001, 0x2407900000000000)

    # Segment 2, Sub-range 4
    distribute_work_manual(0x2407900000000001, 0x246dc00000000000)

    # Segment 3, Sub-range 1
    distribute_work_manual(0x246dc00000000001, 0x2502a80000000000)

    # Segment 3, Sub-range 2
    distribute_work_manual(0x2502a80000000001, 0x259d900000000000)

    # Segment 3, Sub-range 3
    distribute_work_manual(0x259d900000000001, 0x2638700000000000)

    # Segment 3, Sub-range 4
    distribute_work_manual(0x2638700000000001, 0x26a4a00000000000)

    # Segment 4, Sub-range 1
    distribute_work_manual(0x26a4a00000000001, 0x273f880000000000)

    # Segment 4, Sub-range 2
    distribute_work_manual(0x273f880000000001, 0x27da700000000000)

    # Segment 4, Sub-range 3
    distribute_work_manual(0x27da700000000001, 0x2875500000000000)

    # Segment 4, Sub-range 4
    distribute_work_manual(0x2875500000000001, 0x28db800000000000)

    # Segment 5, Sub-range 1
    distribute_work_manual(0x28db800000000001, 0x2976600000000000)

    # Segment 5, Sub-range 2
    distribute_work_manual(0x2976600000000001, 0x2a11400000000000)

    # Segment 5, Sub-range 3
    # distribute_work_manual(0x2a11400000000001, 0x2aac200000000000)

    # Segment 5, Sub-range 4
    # distribute_work_manual(0x2aac200000000001, 0x2b12600000000000)

    # Segment 6, Sub-range 1
    # distribute_work_manual(0x2b12600000000001, 0x2bac480000000000)

    # Segment 6, Sub-range 2
    # distribute_work_manual(0x2bac480000000001, 0x2c47300000000000)

    # Segment 6, Sub-range 3
    # distribute_work_manual(0x2c47300000000001, 0x2ce2100000000000)

    # Segment 6, Sub-range 4
    # distribute_work_manual(0x2ce2100000000001, 0x2d49400000000000)

    # Segment 7, Sub-range 1
    # distribute_work_manual(0x2d49400000000001, 0x2de4200000000000)

    # Segment 7, Sub-range 2
    # distribute_work_manual(0x2de4200000000001, 0x2e7f000000000000)

    # Segment 7, Sub-range 3
    # distribute_work_manual(0x2e7f000000000001, 0x2f19e00000000000)

    # Segment 7, Sub-range 4
    # distribute_work_manual(0x2f19e00000000001, 0x2f80200000000000)

    # Segment 8, Sub-range 1
    # distribute_work_manual(0x2f80200000000001, 0x301b000000000000)

    # Segment 8, Sub-range 2
    # distribute_work_manual(0x301b000000000001, 0x30b5e00000000000)

    # Segment 8, Sub-range 3
    # distribute_work_manual(0x30b5e00000000001, 0x3150c00000000000)

    # Segment 8, Sub-range 4
    # distribute_work_manual(0x3150c00000000001, 0x31b7000000000000)

    # Segment 9, Sub-range 1
    # distribute_work_manual(0x31b7000000000001, 0x3251e00000000000)

    # Segment 9, Sub-range 2
    # distribute_work_manual(0x3251e00000000001, 0x32ecc00000000000)

    # Segment 9, Sub-range 3
    # distribute_work_manual(0x32ecc00000000001, 0x3386a00000000000)

    # Segment 9, Sub-range 4
    # distribute_work_manual(0x3386a00000000001, 0x33edffffffffff00)

     # Segment 10, Sub-range 1
    # distribute_work_manual(0x33edffffffffff01, 0x3487e80000000000)

    # Segment 10, Sub-range 2
    # distribute_work_manual(0x3487e80000000001, 0x3521d00000000000)

    # Segment 10, Sub-range 3
    # distribute_work_manual(0x3521d00000000001, 0x35bcb80000000000)

    # Segment 10, Sub-range 4
    # distribute_work_manual(0x35bcb80000000001, 0x3ffffffffffffffff)