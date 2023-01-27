import sounddevice as sd

sd.default.device = [1,5]

print(sd.query_devices())