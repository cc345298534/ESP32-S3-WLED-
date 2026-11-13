import serial, time, sys

PORT = "COM7"; BAUD = 115200
try:
    s = serial.Serial(PORT, BAUD, timeout=1.5)
except Exception as e:
    print("OPEN_FAIL:", e); sys.exit(1)

time.sleep(0.6)

def get(path):
    s.reset_input_buffer()
    s.write(f"GET {path} HTTP/1.1\r\nHost: wled\r\n\r\n".encode())
    time.sleep(1.6)
    out = b""
    end = time.time()+1.6
    while time.time()<end:
        n=s.in_waiting
        if n: out+=s.read(n)
        else: time.sleep(0.08)
    return out

for p in ["/cfg.json", "/json/cfg"]:
    r = get(p)
    print(f"===== {p} | bytes={len(r)} =====")
    print(r.decode(errors="replace")[:2500])
    print()

s.close()
