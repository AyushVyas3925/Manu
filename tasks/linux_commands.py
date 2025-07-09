import subprocess

# Linux IP and user
LINUX_IP = "your linux server ip"
LINUX_USER = "root"

# Linux native command map
LINUX_COMMANDS = {
    "list files": "ls -l",
    "current directory": "pwd",
    "disk usage": "df -h",
    "memory usage": "free -h",
    "list processes": "ps aux",
    "network status": "ifconfig",
    "cpu info": "lscpu",
    "uptime": "uptime",
    "whoami": "whoami",
    "list users": "cut -d: -f1 /etc/passwd",
    "kernel version": "uname -r",
    "os info": "uname -a",
    "ip address": "hostname -I",
    "list usb devices": "lsusb",
    "list pci devices": "lspci",
    "mounted filesystems": "mount",
    "list block devices": "lsblk",
    "check ports": "ss -tuln",
    "firewall status": "ufw status",
    "active services": "systemctl list-units --type=service",
    "failed services": "systemctl --failed",
    "check cron jobs": "crontab -l",
    "check hostname": "hostname",
    "view dmesg": "dmesg | tail -20",
    "log last reboot": "last reboot",
    "top processes": "top -n 1 -b | head -20",
    "recent logins": "last",
    "disk partitions": "fdisk -l",
    "list hidden files": "ls -a",
    "file permissions": "ls -l",
    "active connections": "netstat -tunapl",
    "available shells": "cat /etc/shells",
    "check bash version": "bash --version",
    "system date": "date",
    "calendar": "cal",
    "find all users": "getent passwd",
    "group list": "getent group",
    "env variables": "printenv",
    "list aliases": "alias"
}

# Docker-specific commands (can expand this)
DOCKER_COMMANDS = {
    "list running containers": "docker ps",
    "list all containers": "docker ps -a",
    "start container": "docker start {container_id_or_name}",
    "stop container": "docker stop {container_id_or_name}",
    "remove container": "docker rm {container_id_or_name}",
    "list images": "docker images",
    "remove image": "docker rmi {image_id_or_name}",
    "build image": "docker build -t {image_name} .",
    "pull image": "docker pull {image_name}",
    "docker version": "docker --version",
    "docker info": "docker info",
    "docker networks": "docker network ls",
    "docker volumes": "docker volume ls",
    "docker stats": "docker stats --no-stream",
    "docker logs": "docker logs {container_id_or_name}",
    "exec into container": "docker exec -it {container_id_or_name} /bin/bash"
}


def run_linux_command(command_name, docker=False):
    command_key = command_name.lower().strip()

    if docker:
        # Handle Docker commands
        if command_key in DOCKER_COMMANDS:
            docker_cmd = DOCKER_COMMANDS[command_key]
        else:
            # Allow raw docker command fallback
            docker_cmd = command_key if command_key.startswith("docker") else f"docker {command_key}"

        ssh_command = f'ssh {LINUX_USER}@{LINUX_IP} "{docker_cmd}"'
    else:
        # Normal Linux command
        if command_key in LINUX_COMMANDS:
            linux_cmd = LINUX_COMMANDS[command_key]
            ssh_command = f'ssh {LINUX_USER}@{LINUX_IP} "{linux_cmd}"'
        else:
            return "❌ Unknown or unsupported Linux command."

    try:
        result = subprocess.check_output(ssh_command, shell=True, stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return f"🔴 SSH Error: {e.output.decode()}"
