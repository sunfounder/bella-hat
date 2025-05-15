from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time
import os
import asyncio
import subprocess
import sys
from io import StringIO
import importlib.util

# Assuming bella_hat, ws2812, vilib, and utils are accessible
from bella_hat.music import Music
from bella_hat.bella import Bella
from bella_hat.utils import run_command
from ws2812 import WS2812

app = FastAPI()

# Static files (CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Initialize Bella, WS2812, and Music
bella = Bella()
bella.motors.reverse([True, False])

config = {
    'rgb_led_count': 32,
    'rgb_enable': True,
    'rgb_color': '#ff0aff',
    'rgb_brightness': 15,
    'rgb_style': 'breathing',
    'rgb_speed': 80,
}

ws2812 = WS2812(config)
ws2812.start()

try:
    music = Music()
except Exception as e:
    print(f"Error initializing music: {e}")
    music = None

# Webcam setup
webcam_address = ""
webcam_done = False
try:
    from vilib import Vilib, utils

    Vilib.camera_start(vflip=True, hflip=False, size=(800, 600))
    Vilib.show_fps()
    Vilib.display(local=False, web=True)

    wlan0, eth0 = utils.getIP()

    if eth0:
        webcam_address += f"http://{eth0}:9000/mjpg\n"
    elif wlan0:
        webcam_address += f"http://{wlan0}:9000/mjpg\n"

    webcam_done = True
except:
    webcam_address = ""
    webcam_done = False

# Global state variables
power = 0
direction = "stop"
eyes_state = True
fan_state = False
connected_clients = set()  # Track connected WebSocket clients


def horn():
    if music is not None:
        _status, _result = run_command('sudo killall pulseaudio')
        music.sound_play_threading('./car-double-horn.wav')

music_play = False

def music_cycle():
    # length = music.sound_length("./slow-trail-Ahjay_Stelino.mp3")
    while music_play:
        if not music.pygame.mixer.music.get_busy():
            music.music_play("./slow-trail-Ahjay_Stelino.mp3")
        time.sleep(.5)

    music.music_stop()

def horn():
        import threading
        global music_play
        if music_play == False:
            music_play = True
            music_thread = threading.Thread(target=music_cycle)
            music_thread.daemon = True
            music_thread.start()
        else:
            music_play = False


async def update_data():
    global direction, eyes_state, fan_state

    batVolt = bella.get_battery_voltage()
    batPerc = bella.get_battery_percentage()
    batstrlen = int(batPerc / 10)
    bat_str = "|" * batstrlen + " " * (10 - batstrlen)
    distance = bella.get_ultrasonic_distance()
    temp = bella.get_temperature()
    hum = bella.get_humidity()
    grayscale = bella.get_grayscales()
    btn_state = bella.read_btn()
    acc = bella.get_acc()
    gyro = bella.get_gyro()
    power_l, power_r = bella.motors.speed()
    fan_state = bella.fan_state
    charging_state = bella.read_charge_status()

    return {
        "webcam_address": webcam_address,
        "direction": direction,
        "bat_str": bat_str,
        "batPerc": batPerc,
        "batVolt": batVolt,
        "distance": distance,
        "temp": temp,
        "hum": hum,
        "acc": acc,
        "gyro": gyro,
        "grayscale": grayscale,
        "fan_state": fan_state,
        "btn_state": btn_state,
        "eyes_state": eyes_state,
        "power_l": power_l,
        "power_r": power_r,
        "charging_state": charging_state
    }

# Background task to send updates to all connected clients
async def send_updates():
    while True:
        if connected_clients:  # Only process if there are connected clients
            data = await update_data()
            # Send to all connected WebSocket clients
            for client in connected_clients.copy():  # Use copy to avoid modification during iteration
                try:
                    await client.send_json(data)
                except Exception:
                    connected_clients.discard(client)  # Remove disconnected clients
        await asyncio.sleep(0.1)  # 100ms interval

@app.on_event("startup")
async def startup_event():
    # Start the background task when the application starts
    asyncio.create_task(send_updates())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Keep the connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Process any commands received from WebSocket if needed
            if data.startswith("action:"):
                action = data.split(":", 1)[1]
                await process_action(action)
    except WebSocketDisconnect:
        connected_clients.discard(websocket)

async def process_action(action: str):
    """Process actions received from WebSocket"""
    global direction, eyes_state
    
    if action in ('forward', 'backward', 'left', 'right', 'stop'):
        direction = action
        if action == 'forward':
            bella.motors.forward(100)
        elif action == 'backward':
            bella.motors.backward(100)
        elif action == 'left':
            bella.motors.turn_left(100)
        elif action == 'right':
            bella.motors.turn_right(100)
        elif action == 'stop':
            bella.motors.stop()
    elif action == 'horn':
        horn()
    elif action == 'fan':
        if bella.fan_state:
            bella.fan_off()
        else:
            bella.fan_on()
    elif action == 'eyes':
        eyes_state = not eyes_state
        if eyes_state:
            ws2812.start()
        else:
            ws2812.stop()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = await update_data()
    return templates.TemplateResponse("index.html", {"request": request, **data})

@app.get("/network", response_class=HTMLResponse)
async def network_test_page(request: Request):
    """Render the network test page"""
    return templates.TemplateResponse("network.html", {"request": request})

@app.post("/run-network-test")
async def run_network_test(
    test_type: str = Form(...),
    iperf_server: str = Form(None),
    bt_mac: str = Form(None)
):
    """Run network tests based on the requested type"""
    # Create a buffer to capture stdout
    output_buffer = StringIO()
    original_stdout = sys.stdout
    output_files = []
    
    try:
        # Redirect stdout to our buffer
        sys.stdout = output_buffer
        
        # Import the test_network module
        spec = importlib.util.spec_from_file_location("test_network", "test_network.py")
        test_network = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_network)
        
        # Run the requested test
        if test_type == 'ble':
            output_files = test_network.ble_test()
        elif test_type == 'bt':
            if bt_mac:
                output_files = test_network.bt_classic_test(bt_mac)
            else:
                print("Error: Bluetooth MAC address is required for BT Classic test")
        elif test_type == 'wifi':
            if iperf_server:
                output_files = test_network.wifi_test(iperf_server=iperf_server)
            else:
                print("Error: iPerf server IP address is required for Wi-Fi test")
        elif test_type == 'wifi5':
            if iperf_server:
                output_files = test_network.wifi_5ghz_test(iperf_server=iperf_server)
            else:
                print("Error: iPerf server IP address is required for Wi-Fi 5GHz test")
        elif test_type == 'fcc':
            if iperf_server:
                output_files = test_network.fcc_rss_emc_tests(iperf_server=iperf_server)
            else:
                print("Error: iPerf server IP address is required for FCC tests")
        elif test_type == 'all':
            if not iperf_server:
                print("Error: iPerf server IP address is required for full test suite")
            else:
                # Use bt_mac if provided, otherwise use default
                bt_address = bt_mac if bt_mac else "9C:76:0E:7C:56:79"
                print(f"Running all tests with iPerf server: {iperf_server} and BT MAC: {bt_address}")
                
                # Run all tests and collect output files
                all_files = []
                
                all_files.extend(test_network.ble_test())
                all_files.extend(test_network.bt_classic_test(bt_address))
                all_files.extend(test_network.wifi_test(iperf_server=iperf_server))
                all_files.extend(test_network.wifi_5ghz_test(iperf_server=iperf_server))
                all_files.extend(test_network.fcc_rss_emc_tests(iperf_server=iperf_server))
                
                output_files = all_files
                print("All tests completed!")
        else:
            print(f"Unknown test type: {test_type}")
        
        # Get the captured output
        output = output_buffer.getvalue()
        
        # Read the content of output files
        file_contents = {}
        for file_path in output_files:
            if file_path is not None:  # Skip None values if any
                file_name = os.path.basename(file_path)
                file_contents[file_name] = test_network.read_output_file(file_path)
        
    except Exception as e:
        output = f"Error running test: {str(e)}"
        file_contents = {}
    finally:
        # Restore stdout
        sys.stdout = original_stdout
    
    # Return JSON response with the test output and file contents
    return JSONResponse(content={
        "output": output,
        "files": file_contents
    })

@app.post("/control")
async def control(action: str = Form(...)):
    await process_action(action)
    # Return JSON data for non-WebSocket clients
    data = await update_data()
    return JSONResponse(content=data)

@app.on_event("shutdown")
async def shutdown_event():
    bella.motors.stop()
    ws2812.stop()
    if webcam_done:
        from vilib import Vilib
        Vilib.camera_close()