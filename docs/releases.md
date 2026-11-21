# Releases

Each release of the program has, for every program (`ortus`, `ortus-mail`, `ortus-drive`, `ortus-chat`) and machine (x86-64 and arm64 Linux), an archive with the program, the install files and the licences of everything in it, and one `SHA256SUMS` file over all the archives, signed. The container image `ghcr.io/ortus-sovereign-cloud/ortus` (tagged `v0.1.0` and `0.1.0`) is signed itself. The chart, `oci://ghcr.io/ortus-sovereign-cloud/charts/ortus`, is signed in the registry, and its release has its own signed `SHA256SUMS`.

The signatures are keyless (Sigstore): each names the workflow that made it, at the release's tag, and is recorded in a public transparency log. Check an archive before installing it:

```sh
sha256sum --check --ignore-missing SHA256SUMS
cosign verify-blob --certificate SHA256SUMS.pem --signature SHA256SUMS.sig \
  --certificate-identity-regexp '^https://github.com/Ortus-Sovereign-Cloud/ortus/\.github/workflows/release\.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com SHA256SUMS
```

The image and the chart:

```sh
cosign verify ghcr.io/ortus-sovereign-cloud/ortus:0.1.0 \
  --certificate-identity-regexp '^https://github.com/Ortus-Sovereign-Cloud/ortus/\.github/workflows/release\.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
cosign verify ghcr.io/ortus-sovereign-cloud/charts/ortus:0.1.0 \
  --certificate-identity-regexp '^https://github.com/Ortus-Sovereign-Cloud/ortus-deploy/\.github/workflows/release\.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

Releases are made only from a tag on `main` whose checks passed.

**Licences.** Ortus is MIT OR Apache-2.0, and takes permissive dependencies only. `LICENSES.md` in each archive lists every dependency of the programs and the web clients with its licence; the phone apps keep their own lists.
