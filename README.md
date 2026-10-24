# Hindi Practice

A static listening library: English → four-second thinking pause → Hindi. Recordings use Devanagari input; reading defaults to Roman Hindi. Select sections to mix, shuffle complete pairs, repeat, and save selected audio on the current device for offline practice.

Serve this folder with `python3 -m http.server 8081`, or open the GitHub Pages deployment. No server, sign-in, speech credentials, or runtime speech generation is needed. Offline storage requires HTTPS or localhost and can be cleared by the browser. The native Android app is preferred for screen-off listening and pausing on disconnected headphones.

## Publish lessons

`python3 tools/publish_library.py /path/to/finished-packs/*.zip`

Review the resulting counts and content, commit, and push to main. GitHub Pages publishes the site and catalog. The native app checks catalog.json on open and periodically while automatic updates are enabled; it downloads validated ZIPs to local storage. Native playback uses local files. Existing packs and stable sentence IDs must be preserved; bump a pack's contentVersion if editing its content. The publisher verifies recording hashes and rejects private metadata in pack manifests.

This repository contains only generic practice content and finished recordings. Never add API keys, configured generator HTML, OAuth credentials, private document links, device identifiers, or signing keys. The generator and Android source remain separate.
