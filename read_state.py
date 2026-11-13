import serial, time, json, sys

PORT = "COM7"
BAUD = 115200
try:
    s = serial.Serial(PORT, BAUD, timeout=1.5)
except Exception as e:
    print("OPEN_FAIL:", e); sys.exit(1)

time.sleep(0.6)
s.reset_input_buffer()
s.write(b'{"v":true}\n')
time.sleep(1.5)
out = b""
end = time.time() + 1.5
while time.time() < end:
    n = s.in_waiting
    if n: out += s.read(n)
    else: time.sleep(0.1)
s.close()

txt = out.decode(errors="replace")
try:
    d = json.loads(txt)
    st = d["state"]; inf = d["info"]; leds = inf["leds"]
    print("固件版本 :", inf.get("ver"))
    print("LED 数量 :", leds.get("count"))
    print("RGBW     :", leds.get("rgbw"))
    print("最大电流 :", leds.get("maxpwr"), "mA")
    print("亮度     :", st.get("bri"))
    print("开关     :", st.get("on"))
    seg0 = st["seg"][0]
    print("颜色     :", seg0.get("col"))
    print("效果fx   :", seg0.get("fx"), " 调色板pal:", seg0.get("pal"))
    wif = inf.get("wifi", {})
    print("WiFi模式 :", "AP热点模式" if wif.get("ap") else "已连WiFi", "| ip:", inf.get("ip") or "(空)")
except Exception as e:
    print("PARSE_FAIL:", e)
    print(txt[:1500])
