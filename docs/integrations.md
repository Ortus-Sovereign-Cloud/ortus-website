# Integrations

**Admin › Backup & restore › Integrations** shows what the installation is connected to.

## Webhooks

An owner adds a webhook with an address and the events it hears of: `record.filed`, `approval.done`, `document.signed`, `task.created`, `person.invited`, `person.joined`, `person.removed`, `backup.restored`. Each event is posted as JSON:

```json
{"event": "record.filed", "id": 1234, "at": 1795197600000, "target": "case-17", "detail": {"record": "r1"}}
```

with the headers `X-Ortus-Event`, `X-Ortus-Delivery`, `X-Ortus-Timestamp` and `X-Ortus-Signature: sha256=<hex>`, the HMAC-SHA256 of `<timestamp>.<body>` with the webhook's secret (shown once, when it is made). Check the signature and that the timestamp is recent. A post that is not taken (an answer other than 2xx) is tried again, 2, 4, 8 … minutes apart, up to 8 tries in all. **Test** sends a `ping`.

The same as an API call:

```sh
curl -X POST https://ortus.ministry.example/api/v1/admin/webhooks \
  -H 'Authorization: Bearer <session token>' -H 'X-Requested-With: ortus' -H 'Content-Type: application/json' \
  -d '{"name":"Cases","url":"https://cases.ministry.example/hook","events":["record.filed","approval.done"]}'
```

## The directory

**Admin › Users & groups** connects LDAP or Active Directory: people and groups come in, names stay up to date.

## Signing in with outside providers

**Admin › Sign-in & devices** adds OpenID Connect and SAML providers (a national eID among them). Ortus is also an OpenID Connect provider for other services.
