# Fancaps Downloader & Web Daemon Interface

An automated image downloader and queue system for \[fancaps.net], built with Python. This repository includes two main components:

* `fancaps-downloader.py`: A **standalone CLI tool** for semi-automatic usage (no web interface).
* `fancaps-daemon.py`: A **fully automated Linux server daemon** with a **Flask-based web UI** to manage and monitor downloads.

> Original CLI tool based on the work by m-patino, improved and extended with automation and interface by AsaTyr.

---
Preview:
![grafik](https://github.com/user-attachments/assets/bd5ce8a3-a8a4-4f9c-937c-5c8b7811e684)

## ✨ Features

* ✅ Download image galleries from fancaps.net (TV, Anime, Movies)
* ✅ CLI mode (`fancaps-downloader.py`) for manual and scripted downloads
* ✅ Daemon mode (`fancaps-daemon.py`) for automatic background processing
* ✅ `queue.txt` + `archive.txt` system for organized tracking
* ✅ Web UI to manage queue entries (add/remove)
* ✅ Read-only archive view in web UI
* ✅ Fully runs as a background service (systemd ready)

---

## 📦 Requirements

* Python 3.8+
* Linux system (tested on Debian/Ubuntu)
* Git
* `beautifulsoup4`, `tqdm`, `flask`

Install with:

```bash
pip install beautifulsoup4 tqdm flask
```

---

## 🧪 CLI Usage (`fancaps-downloader.py`)

### Arguments

* `url`: Single URL to download (season/movie/episode)
* `--output`: Target folder for saving the images (default: `Downloads`)
* `--batch-type`: Type of content in batch mode, either `season` or `movie` (optional)
* `--batch-file`: Path to a text file containing URLs
* `-?`: Show help message

### Supported URLs

* `https://fancaps.net/{tv|anime}/showimages.php?...`
* `https://fancaps.net/{tv|anime}/episodeimages.php?...`
* `https://fancaps.net/movies/MovieImages.php?...`

⚠️ **Note:** If the URL contains `&`, wrap it in **double quotes**.

### Examples:

Download a single episode or season:

```bash
python fancaps-downloader.py --output "Download" "https://fancaps.net/tv/showimages.php?id=1234"
```

Batch download from file:

```bash
python fancaps-downloader.py --batch-file "batch.txt" --batch-type season --output "SeasonDownloads"
```

---

## ⚙️ Installation (Daemon + Web UI)

### 1. Clone the Repository

```bash
cd /opt
sudo git clone https://github.com/AsaTyr2018/fancaps-downloader.git fancaps
cd fancaps
sudo chown -R $USER:$USER .
```

### 2. Setup Directory Structure

```bash
mkdir -p /opt/fancaps/downloads
chmod 775 /opt/fancaps/downloads
```

---

## 🚀 Running the Daemon

Test manually:

```bash
python3 fancaps-daemon.py
```

Run as service:

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

Logs (if configured):

```
/var/log/fancaps-daemon.log
```

---

## 🌐 Running the Web UI

Start manually (default: port 5080):

```bash
cd /opt/fancaps/web
python3 fancaps_web.py
```

Access via:

```
http://<server-ip>:5080
```

### Optional Auto-Start (systemd):

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

## 📁 File Structure Overview

```bash
/opt/fancaps
├── fancaps-downloader.py       # CLI downloader tool
├── fancaps-daemon.py           # Daemon processor
├── queue.txt                   # URLs to download
├── archive.txt                 # Completed downloads
├── downloads/                  # Download target
└── web/
    ├── fancaps_web.py          # Web UI backend
    └── templates/index.html    # Web UI frontend
```

---

## 📝 Notes

* The web interface allows editing `queue.txt` but not `archive.txt`.
* Ensure `queue.txt` is writable by both daemon and Flask UI.
* Avoid port conflicts; default Flask port is 5080.
* You can combine this setup with Samba or any HTTP file server to share the download folder.

---
