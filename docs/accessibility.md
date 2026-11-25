# Accessibility

Ortus aims to meet WCAG 2.2 at level AA on the web and in the iOS and Android apps. That is also what EN 301 549, the European standard for public-sector ICT, asks of web pages and software. This page says how that is checked, what was found and what is still open.

## How it is checked

- **Every screen, automatically.** axe-core runs the WCAG 2.0, 2.1 and 2.2 A and AA rules on every app's screens, signed in, with the sample organisation: on a desktop and a phone, in light and dark, and at 320 px wide (reflow). It also runs with each app's dialogs and menus open, and on the sign-in page.
- **By keyboard.** Every screen is walked with Tab. Each stop must show its focus and must not be hidden behind the phone's bottom bar. Dialogs take focus, close with Escape and give focus back. Menus move with the arrow keys.
- **Text spacing and zoom.** Every screen is laid out again with WCAG's larger line, letter and word spacing at 320 px (the width of 200 % zoom on a small laptop): nothing may scroll sideways or be cut.
- **In the tests.** What was fixed is held by tests in each app's own test suite (focus in dialogs and menus, the 320 px bar), so it cannot quietly break again.
- **Phones.** Screen-reader names, roles and announcements are reviewed in the code: TalkBack on Android, VoiceOver on iOS. Text follows the phone's text size.

## Results (25 November 2026)

axe found no failures on any screen. The keyboard, spacing and phone reviews found these, all fixed:

- Chat's dialogs (new channel, browse channels, turn into a task, send from Drive) and the call's "present what" dialog did not take focus and did not close with Escape.
- The account and language menus, and mail's snooze menu, did not take focus or move with the arrow keys, and Escape did not return to their button.
- A new document left focus nowhere; now its name is selected, ready to type over.
- At 320 px the phone bar could not hold eight places and scrolled sideways.
- On the phones, section titles were not headings, a task's tick was not announced as a checkbox (Android) or a toggle (iOS), and a list that failed to load or the offline banner was not announced when it appeared.

## Known limits

- **Tasks board.** A task's column can be changed in its dialog without dragging. Its order within a column can still only be changed by dragging (WCAG 2.5.7).
- **Screen readers in use.** The checks above are tools and code review. A full pass with NVDA, JAWS, VoiceOver and TalkBack by people who use them every day has not been done yet.
- **What people write.** Documents, messages and files are as accessible as their authors make them. Docs keeps headings, lists and tables as real structure, and exports them that way to Word.

## Reporting a problem

People in an organisation tell its administrators. Problems in Ortus itself go to the issues of the [Ortus repositories](https://github.com/Ortus-Sovereign-Cloud) on GitHub.
