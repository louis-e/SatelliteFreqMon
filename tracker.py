from orbit_predictor.sources import EtcTLESource
from orbit_predictor.locations import Location
from dateutil import tz
from datetime import datetime
import os, time, schedule, telnetlib, subprocess

PASS_WATCHDOG_INTERVAL = 5
GQRX_HOST = '127.0.0.1'
GQRX_PORT = 7356
UTC_TZ = tz.tzutc()
LOCAL_TZ = tz.tzlocal()
GROUNDSTATION_LOCATION = Location(
    name="Munich",
    latitude_deg=48.137154,
    longitude_deg=11.576124,
    elevation_m=520,
)

def utc_to_local(utc):
    utc_time = utc.replace(tzinfo=UTC_TZ)
    local_time = utc_time.astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S")
    return local_time

def gqrx_command(command):
    try:
        tn = telnetlib.Telnet(GQRX_HOST, GQRX_PORT, 2)
        tn.write(command.encode('utf-8') + b'\n')
        response = tn.read_until(b'\n')
        tn.close()
        print(command, response.decode('utf-8').strip())
    except Exception as e:
        print(f"Couldn't execute GQRC command ({e})")

def append_pass_list(tle_path):
    sat_name = open(tle_path).readline().strip()
    sat_frequency = open(tle_path).readlines()[3].strip()
    sat_bandwidth = open(tle_path).readlines()[4].strip()

    source = EtcTLESource(filename=tle_path)
    predictor = source.get_predictor(sat_name)
    predicted_pass = predictor.get_next_pass(GROUNDSTATION_LOCATION)
    pass_list.append([
            predicted_pass.sate_id,
            utc_to_local(predicted_pass.aos),
            utc_to_local(predicted_pass.los),
            str(predicted_pass.los - predicted_pass.aos),
            sat_frequency,
            sat_bandwidth,
            0
        ])


pass_list = [] #NAME AOS LOS DURATION FREQUENCY BANDWIDTH STATUS (0 = waiting for pass, 1 = focus, 2 = done / skip)
def pass_watchdog():
    if len(pass_list) == 0: # First run
        sat_names = []
        for tle_file in os.listdir("sats/"):
            tle_path = "sats/" + tle_file
            sat_name = open(tle_path).readline().strip()
            sat_names.append(sat_name)
            append_pass_list(tle_path)
        print(f"===== Passes calculated for: {sat_names} =====")
        
        print("=== Configuring GQRX...")
        gqrx_command('M WFM 45000')
        gqrx_command('L SQL -150')
        return

    for element in pass_list:
        if element[6] == 0 and datetime.strptime(element[1], "%Y-%m-%d %H:%M:%S") <= datetime.now(): # Acquisition of signal (AOS)
            print(f"=== {element[0]} overpass ({element[1]} - {element[2]} for {element[3]}) on {element[4]}KHz")
            for passes in pass_list:
                if passes[6] == 1:
                    element[6] = 2
                    print(f"Frequency recording already in progress, skipping this pass and keeping focus on current one!")
                    return

            gqrx_command(f'F {element[4]}000')
            gqrx_command(f'M WFM {element[5]}')
            gqrx_command('AOS')
            element[6] = 1

        elif element[6] == 1 and datetime.strptime(element[2], "%Y-%m-%d %H:%M:%S") <= datetime.now(): # Loss of signal (LOS)
            element[6] = 2

            gqrx_command('LOS')
            if 'NOAA' in element[0]:
                print(f"= Decoding {element[0]} pass...")
                # ! TODO: Automatically decode NOAA pass
                #subprocess.Popen(["/home/pi/noaa-apt/noaa-apt","input.wav","-o","output.png"])
            
            pass_list.remove(element)
            for tle_file in os.listdir("sats/"):
                tle_path = "sats/" + tle_file
                sat_name = open(tle_path).readline().strip()
                if element[0] == sat_name:
                    append_pass_list(tle_path)


scheduler = schedule.Scheduler()
scheduler.every(PASS_WATCHDOG_INTERVAL).seconds.do(pass_watchdog)

while True:
    scheduler.run_pending()
    time.sleep(1)