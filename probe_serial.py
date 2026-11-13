import serial, time, sys

PORT = "COM7"
BAUD = 115200

try:
    s = serial.Serial(PORT, BAUD, timeout=1.5)
except Exception as e:
    print("OPEN_FAIL:", e); sys.exit(1)

time.sleep(0.6)

def send_and_read(raw, wait=1.8, label=""):
    s.reset_input_buffer()
    s.write(raw)
    time.sleep(wait)
    out = b""
    # read in small chunks for up to wait+buffer
    end = time.time() + wait
    while time.time() < end:
        n = s.in_waiting
        if n:
            out += s.read(n)
        else:
            time.sleep(0.1)
    print(f"=== {label} | resp bytes={len(out)} ===")
    print(out.decode(errors="replace")[:3000])
    print()

# 1) JSON state request (WLED echoes response over serial)
send_and_read(b'{"v":true}\n', 1.5, "JSON {\"v\":true}")

# 2) HTTP GET info
send_and_read(b"GET /json/info HTTP/1.1\r\nHost: wled\r\n\r\n", 2.0, "GET /json/info")

# 3) HTTP GET cfg (should contain pin/count if HTTP emulation works)
send_and_read(b"GET /json/cfg HTTP/1.1\r\nHost: wled\r\n\r\n", 2.0, "GET /json/cfg")

s.close()
