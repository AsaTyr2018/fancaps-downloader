# Fancaps Downloader & Web Daemon Interface

![grafik](https://github.com/user-attachments/assets/bd5ce8a3-a8a4-4f9c-937c-5c8b7811e684)

## Description
A Python based image crawler and downloader for [fancaps.net]. The project offers two ways to grab screenshots:

* **CLI tool** (`fancaps-downloader.py`) – run manually or in scripts.
* **Daemon + Web UI** (`fancaps-daemon.py`) – background service with a small Flask frontend to manage the download queue.

The original idea comes from m-patino's script and has been expanded with automation and a live interface.

## Features
- Download TV, Anime and Movie galleries
- Automatic crawling from any Fancaps page
- Multi-threaded downloads with progress bars and retry
- Queue/Archive tracking for automated operation
- Flask based web panel to add/remove URLs and view logs
- Runs as a systemd service (daemon and web)

## Installer
A helper script `install.sh` sets up everything under `/opt/fancaps`:

```bash
sudo ./install.sh install   # fresh installation
sudo ./install.sh update    # pull latest changes and restart services
sudo ./install.sh deinstall # remove services and files
```

The installer clones the repository, creates a Python virtual environment, installs dependencies and configures `fancaps-daemon` and `fancaps-web` systemd units.

## Requirements
### For the Daemon
- Python 3.8+
- Linux (tested on Debian/Ubuntu)
- `beautifulsoup4`, `cloudscraper`, `tqdm`

### For the Web Interface
- Flask

All dependencies can be installed via:

```bash
pip install -r requirements.txt
```

## CLI Usage
Run the downloader directly:

```bash
python fancaps-downloader.py [URL] [--output DIR] [--batch-type {season,movie}] [--batch-file FILE]
```

Supported links:
```
https://fancaps.net/{tv|anime}/showimages.php?...  
https://fancaps.net/{tv|anime}/episodeimages.php?...  
https://fancaps.net/movies/MovieImages.php?...
```
Wrap URLs containing `&` in quotes.

## Notes
- `queue.txt` is writable via the web interface, `archive.txt` is read only.
- Web UI listens on port 5080 by default.
- Combine with Samba or any HTTP server to share the downloads folder.

## Used Technologies
- Python + Flask
- BeautifulSoup & Cloudscreper for scraping
- tqdm for progress display
- systemd for service management

