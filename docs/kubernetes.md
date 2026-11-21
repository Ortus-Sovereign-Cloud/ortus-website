# Install on Kubernetes

The chart runs the same program as the one-machine install, one workload per role: web, worker, mail and media. The database is PostgreSQL and files are in S3, bundled in the cluster or your own.

## Install

The bundled database is a CloudNativePG cluster, so install the operator once per cluster first:

```sh
helm install cnpg cloudnative-pg --repo https://cloudnative-pg.github.io/charts -n cnpg-system --create-namespace
helm install ortus oci://ghcr.io/ortus-sovereign-cloud/charts/ortus --version 0.1.0 -n ortus --create-namespace \
  --set publicUrl=https://ortus.ministry.example
```

The chart's version is the program's: it runs the image `ghcr.io/ortus-sovereign-cloud/ortus` of the same version. Check the chart and the image before installing them (see [Releases](releases.html)).

| Setting | Default | What it does |
| --- | --- | --- |
| `publicUrl` | (none) | The address people reach the installation at. |
| `database.mode` | `bundled` | `bundled`: a CloudNativePG cluster. `external`: your PostgreSQL, its URL in `database.external.existingSecret` under `url`. |
| `files.mode` | `bundled` | `bundled`: RustFS in the cluster. `external`: your S3 store (`files.external.endpoint`, keys in `files.external.existingSecret`). |
| `roles.<role>.replicas` | web 2, others 1 | How many of each workload; `roles.mail.enabled` and `roles.media.enabled` turn those roles off. |
| `web.ingress.*` | off | An Ingress for the web role. |
| `roles.mail.hostname`, `roles.mail.tlsSecret` | (none) | The mail host's name and a `kubernetes.io/tls` secret for it (465 and 993 open only with one). |
| `roles.mail.service.type` | `LoadBalancer` | The Service on ports 25, 587 and 143 (and 465, 993). Mail from the internet needs port 25 on a public address. |
| `roles.media.port`, `roles.media.publicAddress` | 40000, (none) | Call media, UDP with a TCP fallback on one port; `publicAddress` is the `ip:port` people in a call reach. |
| `extraEnv` | none | More `ORTUS_*` settings for every container. |
| `backup.*` | on, 03:15, keep 3 | A CronJob running `ortus backup --into` onto its own volume (size it for keep + 1 copies). |

Every pod runs as a non-root user with a read-only root file system and no capabilities; mail listens on high ports inside its pod and the Service maps the standard ones. The image holds one static program and nothing else.
