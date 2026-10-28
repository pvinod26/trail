# Kinly — Family Tracker Website

A responsive family location-sharing website starter with a Leaflet/OpenStreetMap map, Flask API, and SQLite storage.

## Run on Windows
1. Install Python 3.10+.
2. Extract the ZIP.
3. Open Command Prompt in this folder.
4. Run:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   py app.py
   ```
5. Open `http://127.0.0.1:5000`.

## Test on two devices on the same Wi-Fi
- Find the computer's LAN IPv4 address with `ipconfig`.
- On the computer, run `py app.py`.
- On another device connected to the same Wi-Fi, open `http://COMPUTER-IP:5000`.
- The phone browser may require HTTPS for location access. `localhost` is treated as a secure context, but a LAN IP usually is not. For phone location testing, deploy behind HTTPS or use a trusted HTTPS tunnel.

## Important limitations and privacy
- This is a prototype, not a production-secure family tracker. Anyone who can reach the server may register, and all registered members are currently visible to all other users. Do not expose it publicly with real family locations before adding invite-only membership, authentication, TLS, rate limits, retention controls, and stronger authorization.
- A browser page cannot reliably provide continuous background tracking after the page is closed or the OS suspends it. Native Android is better for persistent sharing.
- Distance is straight-line distance. The ETA is a rough estimate based on straight-line distance, not a routed travel ETA. A routing provider should be integrated for proper road routes.
- OpenStreetMap tiles and Leaflet are loaded from public CDNs; internet access is needed for the map.
- Sharing starts only after explicit browser location permission. Pause sharing using the toggle.
