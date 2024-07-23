import network
import uhttpd


def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="MyAccessPoint", authmode=network.AUTH_OPEN)


def stop_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)


def connect_to_wifi(ssid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    while not sta.isconnected():
        pass


def handle_form(req, resp):
    if req.method == "POST":
        ssid = req.form.get("ssid")
        password = req.form.get("password")
        stop_ap()
        connect_to_wifi(ssid, password)
        resp.send_response(200)
        resp.send_header("Content-Type", "text/html")
        resp.end_headers()
        resp.wfile.write(f"Connected to WiFi - ssid: {ssid}!")
    else:
        resp.send_response(200)
        resp.send_header("Content-Type", "text/html")
        resp.end_headers()
        resp.wfile.write(
            b"""
            <html>
            <body>
            <h1>Connect to WiFi</h1>
            <form method="post">
            <label for="ssid">SSID:</label>
            <input type="text" id="ssid" name="ssid"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Connect">
            </form>
            </body>
            </html>
        """
        )


start_ap()
uhttpd.start([("/", handle_form)])
