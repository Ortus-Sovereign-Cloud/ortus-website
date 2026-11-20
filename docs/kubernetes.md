# Install on Kubernetes

The chart runs the same program as the one-machine install, one workload per role: web, worker, mail and media. The database is PostgreSQL and files are in S3, bundled in the cluster or your own.

## Install

The bundled database is a CloudNativePG cluster, so install the operator once per cluster first:

```sh
helm install cnpg cloudnative-pg --repo https://cloudnative-pg.github.io/charts -n cnpg-system --create-namespace
helm install ortus charts/ortus -n ortus --create-namespace
```

| Setting | Default | What it does |
| --- | --- | --- |
| `database.mode` | `bundled` | `bundled`: a CloudNativePG cluster. `external`: your PostgreSQL, its URL in `database.external.existingSecret` under `url`. |
| `files.mode` | `bundled` | `bundled`: RustFS in the cluster. `external`: your S3 store (`files.external.endpoint`, keys in `files.external.existingSecret`). |
| `roles.<role>.replicas` | web 2, others 1 | How many of each workload; `roles.mail.enabled` and `roles.media.enabled` turn those roles off. |
| `web.ingress.*` | off | An Ingress for the web role. |
| `backup.*` | on, 03:15, keep 7 | A CronJob running `ortus backup --into` onto its own volume. |

Every pod runs as a non-root user with a read-only root file system and no capabilities. The image holds one static program and nothing else.

## Calls

The media role needs one UDP port reachable from the people in a call (and a TCP fallback on the same port). Give it a `LoadBalancer` or host port and set `ORTUS_MEDIA_PUBLIC` to the address people reach.
