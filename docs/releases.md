# Releases

Each release has, for every program (`ortus`, `ortus-mail`, `ortus-drive`, `ortus-chat`) and machine (x86-64 and arm64 Linux), an archive with the program, the install files and the licences of everything in it, a `SHA256SUMS` file, and signatures of both. The container image and the chart are signed the same way.

Check an archive before installing it:

```sh
sha256sum --check --ignore-missing SHA256SUMS
cosign verify-blob --certificate SHA256SUMS.pem --signature SHA256SUMS.sig \
  --certificate-identity-regexp 'https://github.com/Ortus-Sovereign-Cloud/ortus/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com SHA256SUMS
```

The signatures are keyless: they name the CI workflow that built the release, and are recorded in a public transparency log.

**Licences.** Ortus is MIT OR Apache-2.0, and takes permissive dependencies only. `LICENSES.md` in each archive lists every dependency with its licence.
