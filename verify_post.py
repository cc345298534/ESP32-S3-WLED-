import serial, time, json, sys

PORT="COM7"; BAUD=115200
s=serial.Serial(PORT, BAUD, timeout=1.5); time.sleep(0.6)

def post_cfg(obj):
    body=json.dumps(obj).encode()
    req=(f"POST /json/cfg HTTP/1.1\r\nHost: wled\r\n"
         f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n").encode()+body
    s.reset_input_buffer(); s.write(req); time.sleep(1.5)

def read_state():
    s.reset_input_buffer(); s.write(b'{"v":true}\n'); time.sleep(1.5)
    out=b""; end=time.time()+1.5
    while time.time()<end:
        n=s.in_waiting
        if n: out+=s.read(n)
        else: time.sleep(0.08)
    try: return json.loads(out.decode(errors="replace"))
    except: return None

# 无害验证：改名字
post_cfg({"n":"USB_POST_TEST"})
time.sleep(1.0)
d=read_state()
print("POST后 name =", d["info"]["name"] if d else "解析失败")
print("POST后 count(运行时) =", d["info"]["leds"]["count"] if d else "?")
print("通道可用?" , "YES" if (d and d["info"]["name"]=="USB_POST_TEST") else "NO / 需重启才反映")
s.close()
