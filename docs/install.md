# Install on one machine

The one-machine install runs the whole of Ortus as one program on Linux with systemd. The data stays on that machine: an SQLite database and a directory of files under `/var/lib/ortus`.

## What you need

- Linux with systemd, 2 CPUs and 4 GB of memory for a few hundred people.
- A name for the installation (for example `ortus.ministry.example`) pointing at the machine, and a TLS reverse proxy in front of Ortus.
- For mail: the machine reachable on ports 25 (incoming mail), 587 (sending from mail apps) and 993 (IMAP).

## Install

Download the release archive for your machine, check its signature (see [Releases](releases.html)), unpack it and run, as root:

```sh
sudo install/install.sh ./ortus
```

This creates the system user `ortus`, keeps all data in `/var/lib/ortus`, writes the settings to `/etc/ortus/ortus.toml` (only the first time) and starts `ortus.service`, listening on 127.0.0.1:7878.

## Settings

Settings are in `/etc/ortus/ortus.toml`; every one can also be given as an `ORTUS_*` variable in `/etc/ortus/ortus.env`, which wins over the file. Secrets (a database password, S3 keys) belong in `ortus.env`.

| Setting | Variable | What it does |
| --- | --- | --- |
| `roles` | `ORTUS_ROLES` | What this program does: `all`, or some of `web`, `worker`, `mail`, `media`, `dav`. |
| `data_dir` | `ORTUS_DATA_DIR` | Where the data lives. |
| `public_url` | `ORTUS_PUBLIC_URL` | The address people reach the installation at, like `https://ortus.ministry.example`. |
| `[web] ip`, `port` | `ORTUS_WEB_IP`, `ORTUS_WEB_PORT` | Where the program listens for the web. |
| `[database] url` | `ORTUS_DATABASE_URL` | PostgreSQL instead of SQLite. |
| `[files.s3]` | `ORTUS_FILES_S3_*` | S3 instead of a directory for files. |

## The first owner

On the first start Ortus prints a setup link in its log. Open it to create the owner of the installation. A new link at any time, until there is an owner:

```sh
sudo -u ortus ORTUS_CONFIG=/etc/ortus/ortus.toml ortus setup-link
```

The owner's first screen is a checklist: the recovery kit, the mail domain and its DNS records, people and groups, sign-in policy, and where the data lives.

## The secrets key

Secrets Ortus keeps in its database (passwords of outside services, signing keys) are sealed with the key in `/var/lib/ortus/secrets.key`, made on the first start. Keep a copy somewhere safe: backups never carry it, and a restore needs it.
