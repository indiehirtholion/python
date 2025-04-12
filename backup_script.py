import os
import shutil
import time
import json
import hashlib
import argparse
import multiprocessing
from datetime import datetime
from subprocess import check_output

"""
# First get the UUID information of the mounted drives/flash
lsblk -o NAME,MOUNTPOINT,UUID,LABEL

# Normal backup (respects time window)
python3 backup_tool.py

# Dry run (simulate copying)
python3 backup_tool.py --dry-run

# Force run even outside allowed hours
python3 backup_tool.py --force

# Limit CPU usage to 4 processes
python3 backup_tool.py --max-procs 4
"""

# ===== CONFIG =====
UUIDS = {
    "8453-95FD": "/media/lexar/blink",
    # Add more UUIDs and mount points
}
DESTINATION_DIR = "/mnt/backup_drive/blink"
ALLOWED_HOURS = (1, 11)
STATE_FILE = "backup_state.json"
RETRY_LIMIT = 3
LOG_DIR = "backup_logs"

os.makedirs(LOG_DIR, exist_ok=True)


# ===== ARGPARSE =====
def parse_args():
    parser = argparse.ArgumentParser(description="USB Drive Backup Utility")
    parser.add_argument("--dry-run", action="store_true", help="Simulate backup without copying")
    parser.add_argument("--force", action="store_true", help="Run regardless of time window")
    parser.add_argument("--max-procs", type=int, default=min(8, multiprocessing.cpu_count()), help="Max parallel workers")
    return parser.parse_args()


# ===== HELPERS =====

def current_hour():
    return datetime.now().hour

def wait_until_allowed(force=False):
    while not force and not (ALLOWED_HOURS[0] <= current_hour() < ALLOWED_HOURS[1]):
        print("Waiting for allowed backup window...")
        time.sleep(600)

def get_mounted_uuid_paths():
    output = check_output("lsblk -o UUID,MOUNTPOINT -nr", shell=True).decode().splitlines()
    mount_map = {}
    for line in output:
        parts = line.split(None, 1)  # split into at most 2 parts
        if len(parts) == 2:
            uuid, mount = parts
            if uuid and mount:
                mount_map[uuid.strip()] = mount.strip()
    return {uuid: mount_map.get(uuid) for uuid in UUIDS if uuid in mount_map}

def compute_sha256(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_and_copy(args):
    src_file, dst_file, dry_run = args
    for attempt in range(RETRY_LIMIT):
        try:
            if dry_run:
                return {"file": dst_file, "status": "simulated"}
            shutil.copy2(src_file, dst_file)
            if compute_sha256(src_file) == compute_sha256(dst_file):
                return {"file": dst_file, "status": "verified"}
            else:
                raise ValueError("Hash mismatch")
        except Exception as e:
            print(f"Retry {attempt+1}/{RETRY_LIMIT} failed for {src_file}: {e}")
            time.sleep(1)
    return {"file": dst_file, "status": "failed"}

def load_state():
    return json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {"drive_index": 0, "dir_index": 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def log_results(date_str, results, dry_run=False):
    tag = "dry_run" if dry_run else "backup"
    txt_log = os.path.join(LOG_DIR, f"{tag}_{date_str}.txt")
    json_log = os.path.join(LOG_DIR, f"{tag}_{date_str}.json")

    with open(txt_log, 'w') as f_txt, open(json_log, 'w') as f_json:
        f_txt.write(f"Backup Date: {date_str}\n\n")
        for result in results:
            f_txt.write(f"{result['status'].upper()}: {result['file']}\n")
        json.dump(results, f_json, indent=2)

def backup_directory(src_dir, dst_base, date_str, dry_run, max_procs):
    dst_dir = os.path.join(dst_base, os.path.basename(src_dir) + "_" + date_str)
    if not dry_run:
        os.makedirs(dst_dir, exist_ok=True)

    jobs = []
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel_path)
        if not dry_run:
            os.makedirs(dst_root, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)
            jobs.append((src_file, dst_file, dry_run))

    with multiprocessing.Pool(processes=max_procs) as pool:
        results = pool.map(verify_and_copy, jobs)

    return results


# ===== MAIN =====

def main():
    args = parse_args()
    state = load_state()
    mounted_paths = get_mounted_uuid_paths()
    mounted_drives = list(mounted_paths.items())

    while state["drive_index"] < len(mounted_drives):
        wait_until_allowed(force=args.force)

        uuid, mount_point = mounted_drives[state["drive_index"]]
        if not mount_point or not os.path.exists(mount_point):
            print(f"Drive {uuid} not found. Skipping...")
            state["drive_index"] += 1
            state["dir_index"] = 0
            save_state(state)
            continue

        all_dirs = [os.path.join(mount_point, d) for d in os.listdir(mount_point)
                    if os.path.isdir(os.path.join(mount_point, d))]

        for i in range(state["dir_index"], len(all_dirs)):
            wait_until_allowed(force=args.force)

            src_dir = all_dirs[i]
            date_str = datetime.now().strftime("%Y-%m-%d")
            print(f"{'Simulating' if args.dry_run else 'Backing up'} {src_dir}...")
            results = backup_directory(src_dir, DESTINATION_DIR, date_str, args.dry_run, args.max_procs)
            log_results(date_str, results, dry_run=args.dry_run)

            # Save state after each directory
            state["dir_index"] += 1
            save_state(state)

        state["drive_index"] += 1
        state["dir_index"] = 0
        save_state(state)

    print("✅ Done!" if not args.dry_run else "✅ Dry run complete!")

if __name__ == "__main__":
    main()
