# Modified Fancaps Downloader & Web Interface (Original by m-patino) 

An automated image downloader and queue system for \[fancaps.net], built with Python and Flask. This setup includes:

* A **daemon** that processes URLs listed in `queue.txt` and archives them in `archive.txt`.
* A **Flask-based web interface** to manage the download queue and view the archive.
* Optional integration with Samba or web access for downloaded files.

---

## Features

* ✅ Fully automated download of episodic or movie image galleries from fancaps.net
* ✅ CLI and daemon mode for hands-off processing
* ✅ Queue and archive system via text files
* ✅ Web interface to manage `queue.txt`
* ✅ Read-only archive view
* ✅ Runs as a background service

---

## Requirements

* Python 3.8+
* Linux system (tested on Debian/Ubuntu)
* Git
* beautifulsoup4
* tqdm
* Flask (`pip install flask`)

---

## Installation

### 1. Clone the Repository

```bash
cd /opt
sudo git clone https://github.com/AsaTyr2018/fancaps-downloader.git fancaps
cd fancaps
sudo chown -R $USER:$USER .
```

### 2. Install Flask

```bash
pip3 install flask
```

### 3. Directory Structure

```bash
/opt/fancaps
├── fancaps-downloader.py       # CLI + logic
├── fancaps-daemon.py           # Background processor
├── queue.txt                   # List of URLs to download
├── archive.txt                 # Already downloaded URLs
├── downloads/                 # Output directory
├── web/
│   ├── fancaps_web.py          # Flask interface
│   └── templates/index.html    # HTML template
```

### 4. Setup Download Directory

```bash
mkdir -p /opt/fancaps/downloads
chmod 775 /opt/fancaps/downloads
```

---

## Running the Daemon

To test manually:

```bash
python3 fancaps-daemon.py
```

To run in background on boot, add this systemd unit:

```ini
# /etc/systemd/system/fancaps-daemon.service
[Unit]
Description=Fancaps Download Daemon
After=network.target

[Service]
Type=simple
User=yourusername
ExecStart=/usr/bin/python3 /opt/fancaps/fancaps-daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fancaps-daemon
sudo systemctl start fancaps-daemon
```

Logs are written to:

```
/var/log/fancaps-daemon.log
```

---

## Running the Web Interface

To launch the Flask app (on e.g. port 5080):

```bash
cd /opt/fancaps/web
python3 fancaps_web.py
```

Access via:

```
http://<server-ip>:5080
```

### Flask Auto-Start (optional)

Create another systemd unit:

```ini
# /etc/systemd/system/fancaps-web.service
[Unit]
Description=Fancaps Web UI
After=network.target

[Service]
Type=simple
User=yourusername
ExecStart=/usr/bin/python3 /opt/fancaps/web/fancaps_web.py
WorkingDirectory=/opt/fancaps/web
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl enable fancaps-web
sudo systemctl start fancaps-web
```

---

## Notes

* `queue.txt` must be writable by the daemon and web interface.
* The web interface supports adding/removing entries in the queue.
* The archive section is read-only.
* Make sure no other service is using port 5080.

---

