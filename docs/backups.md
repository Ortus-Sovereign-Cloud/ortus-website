# Backups and restore

Ortus keeps two kinds of copies, and both restore into either shape: a backup of the one-machine install restores into the chart, and back.

## Nightly backups

`ortus-backup.timer` (one machine) or the backup CronJob (Kubernetes) writes a whole backup every night and keeps seven. Copy them off the machine. By hand:

```sh
sudo -u ortus ORTUS_CONFIG=/etc/ortus/ortus.toml ortus backup /srv/backups/before-upgrade
ortus check-backup /srv/backups/before-upgrade
```

To restore: stop Ortus, give it an empty data directory (or an empty database and bucket), then `ortus restore <backup>` and start Ortus. Put the secrets key back first.

## Restore points

Ortus also takes a restore point every hour and keeps one an hour for 48 hours, one a day for 30 days and one a week for a year. A file's contents are stored once however many points name it. Points go to `ORTUS_BACKUP_DIR` (by default `<data_dir>/backups`) or an S3 bucket of their own (`ORTUS_BACKUP_S3_ENDPOINT`, `_BUCKET`, `_REGION`, `_ACCESS_KEY`, `_SECRET_KEY`, `_ROOT`). Each point's manifest is sealed with the installation's key, so a point changed in the backup store is refused.

**Admin › Backup & restore** brings back one person's mail folder, Drive folder or calendar as it was at a point, into a new place beside theirs; nothing of theirs is overwritten. With **Self-restore** on, people do it for themselves.

A whole point becomes an ordinary backup with:

```sh
ortus export-point 20261120-180000 /srv/backups/point
```

## The restore test

Once a month, and whenever an owner asks (**Test a restore now**), Ortus restores the newest point whole into a scratch installation, checks every table's rows, every file, and that its keys open what it sealed, and records how long it took. The result is on the backup screen.
