# Backups and restore

Ortus keeps two kinds of copies, and both restore into either shape: a backup of the one-machine install restores into the chart, and back.

## Nightly backups

`ortus-backup.timer` (one machine; keeps seven, in `/var/lib/ortus/backups`) or the backup CronJob (Kubernetes; keeps three) writes a whole backup every night. Copy them off the machine. By hand:

```sh
sudo ortusctl backup /var/lib/ortus/backups/before-upgrade
sudo ortusctl check-backup /var/lib/ortus/backups/before-upgrade
```

A restore goes into an empty database and file store only. On one machine with SQLite:

```sh
sudo systemctl stop ortus
sudo mv /var/lib/ortus /var/lib/ortus.old
sudo install -d -o ortus -g ortus -m 0750 /var/lib/ortus
sudo cp -p /var/lib/ortus.old/secrets.key /var/lib/ortus/
sudo ortusctl restore /var/lib/ortus.old/backups/before-upgrade
sudo systemctl start ortus
```

With PostgreSQL or S3, point the settings at an empty database and bucket instead. The secrets key must be the old installation's.

## Restore points

Ortus also takes a restore point every hour and keeps one an hour for 48 hours, one a day for 30 days and one a week for a year. A file's contents are stored once however many points name it. Points go to `ORTUS_BACKUP_DIR` (by default `<data_dir>/backups`) or an S3 bucket of their own (`ORTUS_BACKUP_S3_ENDPOINT`, `_BUCKET`, `_REGION`, `_ACCESS_KEY`, `_SECRET_KEY`, `_ROOT`). Each point's manifest is sealed with the installation's key, so a point changed in the backup store is refused.

**Admin › Backup & restore** brings back one person's mail folder, Drive folder or calendar as it was at a point, into a new place beside theirs; nothing of theirs is overwritten. With **Self-restore** on, people do it for themselves.

A whole point becomes an ordinary backup with:

```sh
sudo ortusctl export-point 20261120-180000 /var/lib/ortus/backups/point
```

## The restore test

Once a month, and whenever an owner asks (**Test a restore now**), Ortus restores the newest point whole into a scratch installation, checks every table's rows, every file, and that its keys open what it sealed, and records how long it took. The result is on the backup screen.
