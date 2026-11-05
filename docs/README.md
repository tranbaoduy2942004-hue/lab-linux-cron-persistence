# Linux Cron Persistence Detection & Response

Lab ID: lab-linux-cron-persistence

## Topology
- linux-host: 172.29.113.10
- soc: 172.29.113.20

## Installation (Labtainer HOST)
imodule https://raw.githubusercontent.com/tranbaoduy2942004-hue/lab-linux-cron-persistence/main/imodule.tar
labtainer lab-linux-cron-persistence

## Practice

### 1. LINUX-HOST: Create cron jobs
bash /usr/local/bin/manage_cron.sh normal
bash /usr/local/bin/manage_cron.sh attack
crontab -l

### 2. LINUX-HOST: Verify real execution
tail /home/ubuntu/cron-lab/executions.log

Wait until both NORMAL_CRON_EXECUTED and
PERSISTENCE_CRON_EXECUTED appear.

### 3. SOC: Collect and detect
python3 /usr/local/bin/soc_cron.py collect
python3 /usr/local/bin/soc_cron.py detect

Expected: CRON_PERSISTENCE_DETECTED

### 4. LINUX-HOST: Remove persistence
bash /usr/local/bin/manage_cron.sh cleanup
crontab -l

### 5. SOC: Verify remediation
python3 /usr/local/bin/soc_cron.py verify

Expected: PERSISTENCE_REMOVED_VERIFIED

### 6. HOST: Checkwork
checkwork lab-linux-cron-persistence

Expected: 5/5 Y

## Safety
The simulated persistence only writes a local
marker to executions.log.
No malicious payload or external connection.
