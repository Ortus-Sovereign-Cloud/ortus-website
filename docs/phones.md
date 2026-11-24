# Phones

The Ortus apps for iOS and Android cover mail, chat, calendar, files, documents, approvals and tasks, notifications, search and the administrator's essentials.

**The phone as a key.** On first start the app takes the installation's address and the code from the person's welcome letter. Then the phone becomes their key: it makes a passkey that never leaves the phone's secure hardware (the Secure Enclave, the Android Keystore), guarded by Face ID, a fingerprint or the phone's passcode, and registers it like any passkey. Signing documents asks for it again.

**What IT can see:** the app's version, the system's version, and whether the phone is encrypted. Not photos, messages, calls or location. A lost phone's key is turned off in **Admin › Users & groups**.

## Notifications

New Important mail, mentions, approvals and alerts can reach phones while the app is closed. They are off until an administrator turns them on in **Admin › Integrations › Phone notifications**. A push carries only a reference to the notification: the phone fetches the text from the installation itself, with a token that can read that person's notifications and nothing else. Quiet hours and do-not-disturb hold pushes back; a phone stops getting them when its person signs out.

**iPhone.** Apple delivers pushes to the Ortus Workspace app only for the holder of the publisher's key, so an installation hands each push to a push gateway, by default the publisher's (`https://ortus.cc/api/v1/push/gateway`). The gateway receives the phone's push address, the notification's reference and the installation's address; it keeps none of it and sees no content. An organisation that builds and signs the app itself sets its own key and is its own gateway:

| Variable | What it does |
| --- | --- |
| `ORTUS_APNS_KEY_FILE` | Apple's push key (the `.p8` file). |
| `ORTUS_APNS_KEY_ID`, `ORTUS_APNS_TEAM_ID` | The key's id and the team it belongs to. |
| `ORTUS_APNS_TOPIC` | The app's bundle id (default `cc.ortus.app`). |

**Android.** Without Google's services: the app uses [UnifiedPush](https://unifiedpush.org). The person installs a distributor app (ntfy, for example, which can use the organisation's own ntfy server); the installation posts to the address it gives. Without a distributor the app works as before and shows notifications when opened.
