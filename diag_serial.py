import serial, time, serial.tools.list_ports

ports = [p.device for p in serial.tools.list_ports.comports()]
print("PORTS:", ports)

# pick ESP32-S3 (303A) if COM7 not present
port = 'COM7'
if port not in ports:
    cand = [p.device for p in serial.tools.list_ports.comports() if '303A' in (p.hwid or '')]
    port = cand[0] if cand else None
    print("COM7 missing, using", port)

if not port:
    print("NO ESP32 COM FOUND")
    raise SystemExit

try:
    ser = serial.Serial(port, 115200, timeout=1)
except Exception as e:
    print("OPEN FAIL (port likely busy on your side):", e)
    raise SystemExit

time.sleep(0.6)
# send WLED info request
ser.write(b'{"v":true}\n')
time.sleep(2.5)
n = ser.in_waiting
buf = ser.read(n if n else 4000)
print("=== RESPONSE (first 1500 chars) ===")
print(buf.decode(errors='replace')[:1500])
ser.close()
