# Calls

Calls run through Ortus's own media server, the `media` role: each person's audio, video and screen go to it and on to the others in the call, encrypted in transit (DTLS-SRTP) and never decoded. One machine is enough for many small calls; the media role can also run on a machine of its own.

## The media server

| Setting | Variable | What it does |
| --- | --- | --- |
| `roles` | `ORTUS_ROLES` | Include `media` (or `all`). |
| | `ORTUS_MEDIA_LISTEN` | Where it takes media: one UDP port, and ICE over TCP on the same port. Default `0.0.0.0:40000`. |
| | `ORTUS_MEDIA_PUBLIC` | The address browsers and phones send media to, `ip:port`. Set it when the machine is behind NAT (a cloud provider's private address): the public IP and the same port. |

Open the port in the firewall for UDP and TCP (`40000/udp`, `40000/tcp`). UDP is the normal path; TCP on the same port is for networks that block UDP.

## Networks that allow only web ports

Some networks (offices, hotels, public Wi-Fi) let through only HTTPS on port 443. For them Ortus has a TURN relay: browsers and the apps reach it over TLS on 443 and their media goes through it to the media server. They try the direct path first and use the relay only when that fails. The relay forwards to your media server only, with short-lived credentials handed out when someone joins a call, so it cannot be used as a relay for anything else.

| Setting | Variable | What it does |
| --- | --- | --- |
| | `ORTUS_TURN_LISTEN` | Where the relay listens, plain TCP on this machine, like `127.0.0.1:3478`. |
| | `ORTUS_TURN_URL` | How browsers reach it, like `turns:turn.ministry.example:443?transport=tcp`. |

Both are needed; the relay runs with the media role. Port 443 is usually taken by your web proxy, so give the relay its own name (`turn.ministry.example`, pointing at the same machine) and have the proxy pass that name's TLS connections, after their handshake, to `ORTUS_TURN_LISTEN` instead of serving them as a web site. With [rws](https://rws8.tech) (18.39 or later):

```toml
tls_tunnels = ["turn.ministry.example=127.0.0.1:3478"]   # before the first [table]
domains     = ["ortus.ministry.example", "turn.ministry.example"]   # the name needs a certificate
```

Any TLS proxy that can route by name (SNI) and forward the decrypted stream as TCP works the same way.

To check it: join a call with `?ice=relay` added to its address (`…/calls?room=…&ice=relay`). The browser then uses only the relay; if the call connects, the path through port 443 works.
