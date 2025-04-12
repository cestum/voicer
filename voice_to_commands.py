from whisper_cpp_python import Whisper
import sounddevice as sd
import numpy as np
import asyncio
from bleak import BleakClient, BleakScanner
import struct
import sys
import random
# This program uses whisper_cpp python library (modified)
# Whisper.cpp setup
model = Whisper(model_path="./whisper.cpp/models/ggml-base.en.bin")
SAMPLE_RATE = 16000
RECORD_SECONDS = 3

# Bluetooth setup
HUB_NAME = "S3"
COMMAND_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# Command mapping
COMMANDS = {
    "go straight": b"fwd",
    "turn left": b"lft",
    "turn right": b"rgt",
    "stop": b"stp"
}

COMMANDS_KEYS = list(COMMANDS.keys())

def record_audio():
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    return np.squeeze(audio)

async def main():
    # Bluetooth connection
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if not device:
        print("Hub not found")
        return
    
    ready_event = asyncio.Event()
    def handle_rx(_, data: bytearray):
        print(f"received text from spike ")
        if data[0] == 0x01:  # "write stdout" event (0x01)
            print(f"received text from spike2 ")
            payload = data[1:]
            if payload == b"rdy":
                ready_event.set()
            else:
                print("Received:", payload)

    async def send_command(client, command):
        bcommand = COMMANDS.get(command)
        if not bcommand:
            print(f"Not a valid command {command}")
            return
        await ready_event.wait()
        # Prepare for the next ready event.
        ready_event.clear()        
        print(f"Recognized Command: {command}")            
        await client.write_gatt_char(COMMAND_CHAR_UUID, b"\x06" + bcommand, response=True)
        print(f"Sent Command: {command}")
        if command == "stop":
            print("Stopping program")
            await client.disconnect()
            sys.exit(0)
                                
    async with BleakClient(device) as client:
        print("Connected to hub")
        # Subscribe to notifications from the hub.
        await client.start_notify(COMMAND_CHAR_UUID, handle_rx)        
        while True:
            # Record and transcribe
            audio = record_audio()
            raw_text = model._full(audio)
            text = raw_text["text"]
            
            # testing purpose only - Comment above and uncomment below for random testing
            # rand_command = random.randint(0,3)
            # text = COMMANDS_KEYS[rand_command]
            
            # Send command
            await send_command(client, text)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())