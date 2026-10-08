# Lantern

**Play classic text adventures in your browser.** Lantern is a playable Z-machine game interface, beginning with Zork I, with optional self-hosting and experiments in portable saves and player-held signatures.

<p align="center">
  <a href="https://johnrigler.github.io/lantern/"><img src="assets/lantern-preview.svg" alt="Preview of Lantern playing Zork I in a phone-shaped terminal" width="600"></a>
</p>

<p align="center">
  <a href="https://johnrigler.github.io/lantern/lantern.html"><strong>▶ PLAY LANTERN NOW</strong></a>
  &nbsp; · &nbsp;
  <a href="https://johnrigler.github.io/lantern/">Watch the animated preview</a>
</p>

The preview above shows the game interface. The [GitHub Pages homepage](https://johnrigler.github.io/lantern/) animates commands and responses, then loops. **The Play link opens the real interactive client**, which connects to the default Lantern game server at `https://rigler.org/lantern/`. Availability depends on that server being online and having the game files installed.

## How it works

Choose a game, enter commands such as `north`, `open mailbox`, or `inventory`, and read what happens. The browser is a thin client; a Python server runs `dfrotz` with a compatible Z-machine story file. Save and load controls are available in the interface.

You can change the game server under **Settings**, including using your own server instead of `rigler.org`.

```text
Browser (GitHub Pages, IPFS, or local hosting)
    ↓ HTTP API
Lantern Python server
    ↓
dfrotz + your Z-machine story files
```

## Run your own server

Lantern is not dependent on the default host. On a Linux machine, install Python and Frotz, provide compatible story files, and run the server:

```sh
sudo apt install frotz
python3 lantern.py
```

By default the server listens on port `7788`. For a remotely hosted HTTPS client, expose the API behind an HTTPS reverse proxy. The client can then use your server URL in **Settings**.

For details, see [Lantern setup and API notes](LANTERN.md), the [self-hosting section](https://johnrigler.github.io/lantern/#self-hosting), and [About Lantern](about.html).

## Background and experiments

Lantern began as **Zarkmid**, a project named for the fictional currency in Infocom's Zork games. Earlier experiments explored referencing game saves from Dogecoin transactions. The current implementation uses Python and Frotz, and explores user-held cryptographic identities, portable game saves, and optional payments for independently operated hosting.

The game files are separate from the client and server code. Only distribute story files you have rights to use. For Frotz, see [the Frotz project](https://gitlab.com/DavidGriffith/frotz); for historical Infocom downloads, see [infocom-if.org](https://infocom-if.org/downloads/downloads.html).

**Links:** [Play the game](https://johnrigler.github.io/lantern/lantern.html) · [Lantern homepage](https://johnrigler.github.io/lantern/) · [Technical notes](LANTERN.md) · [Attestation proposal](ATTESTATION-PROPOSAL.md)
