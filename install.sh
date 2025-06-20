#!/usr/bin/env bash

set -e

REPO_URL="https://github.com/AsaTyr2018/fancaps-downloader.git"
INSTALL_DIR="/opt/fancaps"
DAEMON_SERVICE="/etc/systemd/system/fancaps-daemon.service"
WEB_SERVICE="/etc/systemd/system/fancaps-web.service"
RUN_USER="${SUDO_USER:-$(whoami)}"

create_services() {
    cat <<SERVICE | sudo tee "$DAEMON_SERVICE" > /dev/null
[Unit]
Description=Fancaps Download Daemon
After=network.target

[Service]
Type=simple
User=${RUN_USER}
ExecStart=/usr/bin/python3 ${INSTALL_DIR}/fancaps-daemon.py
WorkingDirectory=${INSTALL_DIR}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

    cat <<SERVICE | sudo tee "$WEB_SERVICE" > /dev/null
[Unit]
Description=Fancaps Web UI
After=network.target

[Service]
Type=simple
User=${RUN_USER}
ExecStart=/usr/bin/python3 ${INSTALL_DIR}/web/fancaps_web.py
WorkingDirectory=${INSTALL_DIR}/web
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE
}

install_app() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "Installation already exists at $INSTALL_DIR"
    else
        sudo git clone "$REPO_URL" "$INSTALL_DIR"
    fi
    sudo mkdir -p "$INSTALL_DIR/downloads"
    sudo touch "$INSTALL_DIR/queue.txt" "$INSTALL_DIR/archive.txt"
    sudo chown -R "$RUN_USER":"$RUN_USER" "$INSTALL_DIR"
    sudo chmod -R 755 "$INSTALL_DIR"
    create_services
    sudo systemctl daemon-reload
    sudo systemctl enable fancaps-daemon fancaps-web
    sudo systemctl start fancaps-daemon fancaps-web
    echo "Installation complete"
}

update_app() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        cd "$INSTALL_DIR"
        sudo -u "$RUN_USER" git pull
        sudo systemctl restart fancaps-daemon fancaps-web
        echo "Update complete"
    else
        echo "Installation not found at $INSTALL_DIR" >&2
        exit 1
    fi
}

deinstall_app() {
    sudo systemctl stop fancaps-daemon fancaps-web || true
    sudo systemctl disable fancaps-daemon fancaps-web || true
    sudo rm -f "$DAEMON_SERVICE" "$WEB_SERVICE"
    sudo systemctl daemon-reload
    sudo rm -rf "$INSTALL_DIR"
    echo "Deinstallation complete"
}

case "$1" in
    install)
        install_app
        ;;
    update)
        update_app
        ;;
    deinstall)
        deinstall_app
        ;;
    *)
        echo "Usage: $0 {install|update|deinstall}"
        exit 1
        ;;
esac


