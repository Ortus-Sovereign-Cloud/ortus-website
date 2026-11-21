# Upgrades

Running `install.sh` again with a new program is the upgrade on one machine: it takes a backup first (into `/var/lib/ortus/backups`), keeps the old program as `/usr/local/bin/ortus.previous`, and puts it back when the new one does not come up. On Kubernetes, `helm upgrade ortus oci://ghcr.io/ortus-sovereign-cloud/charts/ortus --version <new>`.

Every program brings the database up to date when it starts, and refuses a database newer than it knows. Going back after an upgrade that changed the database therefore means restoring the backup taken before it: take one before every upgrade (`kubectl create job --from=cronjob/<release>-backup before-upgrade` on Kubernetes).
