# Sizing

How big a machine an organisation needs, from a load test that runs every week against the release program (the `load` workflow in the program's repository: `stories/load/load.ts`).

## What is measured

A thousand people are signed in at once, each with twenty messages in their mailbox and all of them in one busy channel. For five minutes each does what a working day does, about once every six seconds: reads and sends chat, opens the inbox and a message, receives mail, looks at the week's calendar and their tasks, finds colleagues, lists and uploads files, makes documents, searches. Everyone also has an end-to-end device with cross-signing keys and a key backup of 200 room keys, in end-to-end rooms of 50: senders fetch a room's devices and who vouches for whom, new room keys go to the backup, and now and then a device restores all of it. Then the pauses go and more and more people act at once, to see where the installation leaves its budget: 400 ms for 95 % of reads, 1 s for writes, almost no errors.

The installation is the cluster shape: the program with PostgreSQL 17 and S3-compatible storage, all on one 4-core, 16 GB GitHub runner, together with the load maker. The numbers are therefore a floor: on a machine of its own Ortus has more room.

## A thousand people (27 November 2026)

- 49,976 operations in 5 minutes (167 a second), no errors.
- The program used under half a core on average and at most 122 MB of memory.
- 95 % of the working day's operations answered in under 50 ms. End-to-end trust: a 50-person room's devices with their signatures in 17 ms, a backup upload in 26, a full restore of the backup in 12.

| Without pauses | Operations a second | Reads (p95) | Writes (p95) |
|---:|---:|---:|---:|
| 25 at once | 499 | 213 ms | 275 ms |
| 50 at once | 433 | 549 ms | 670 ms |
| 100 at once | 431 | 1.1 s | 849 ms |
| 200 at once | 441 | 2.2 s | 1.2 s |

Beyond 25 at once without pauses the shared runner's four cores are full (PostgreSQL, the S3 store and the load maker share them) and requests wait for one of the 16 database connections.

## What to start with

- **Up to about 1,000 people**: one machine with 4 cores and 8 GB of memory runs Ortus, PostgreSQL and the files comfortably; the one-machine install (SQLite) suits a few hundred.
- **More, or more at once**: give PostgreSQL its own machine, raise `ORTUS_DATABASE_MAX_CONNECTIONS` with it (16 by default), and run more web pods on Kubernetes.
- **Disk**: mail and files are most of it. Plan for each person's mail and files, plus the backups and hourly restore points (see [Backups](backups.html)).
- **Calls** are separate: the media server forwards video and needs bandwidth more than cores (see [Calls](calls.html)).

`ORTUS_SLOW_MS` logs requests slower than that many milliseconds, with their database time, and `ORTUS_SERVER_TIMING` adds that time to each answer's `Server-Timing` header, for finding out what is slow on an installation of your own.
