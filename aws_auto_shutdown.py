"""
Auto-shutdown script to save money
Shuts down EC2 instance after X minutes of inactivity
Run in background: nohup python aws_auto_shutdown.py &
"""

import time
import subprocess
import os
from datetime import datetime

# Configuration
IDLE_MINUTES = 30  # Shutdown after 30 minutes of no activity
CHECK_INTERVAL = 60  # Check every 60 seconds

def get_last_activity():
    """Check when last command was run"""
    try:
        # Check last command time in bash history
        result = subprocess.run(
            ["stat", "-c", "%Y", os.path.expanduser("~/.bash_history")],
            capture_output=True,
            text=True
        )
        return int(result.stdout.strip())
    except:
        return int(time.time())

def shutdown_instance():
    """Shutdown the EC2 instance"""
    print(f"[{datetime.now()}] No activity for {IDLE_MINUTES} minutes. Shutting down...")
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def main():
    print(f"[{datetime.now()}] Auto-shutdown monitor started")
    print(f"Will shutdown after {IDLE_MINUTES} minutes of inactivity")
    
    last_activity = get_last_activity()
    
    while True:
        time.sleep(CHECK_INTERVAL)
        
        current_activity = get_last_activity()
        idle_seconds = time.time() - current_activity
        idle_minutes = idle_seconds / 60
        
        if idle_minutes >= IDLE_MINUTES:
            shutdown_instance()
            break
        else:
            remaining = IDLE_MINUTES - idle_minutes
            print(f"[{datetime.now()}] Idle for {idle_minutes:.1f} min. Shutdown in {remaining:.1f} min")

if __name__ == "__main__":
    main()
