from ADSB_Encoder import *

def listCoords(start_lat, start_lon, start_alt, end_lat, end_lon, end_alt, speed):
    from geopy import distance

    # Distance across surface of earth
    flatDistance = distance.distance((start_lat, start_lon), (end_lat, end_lon)).miles
    # Factor in altitude
    end_alt_miles = end_alt * 0.000189394
    start_alt_miles = start_alt * 0.000189394
    totalDistance = math.sqrt(flatDistance**2 + (end_alt_miles - start_alt_miles)**2)
    print("Total Distance: ", totalDistance)
    # 3D distance divided by speed and converted to seconds
    numCoords = int((totalDistance / speed) * 3600)
    
    # Calculate steps in each direction
    step_lat = (end_lat - start_lat) / numCoords
    step_lon = (end_lon - start_lon) / numCoords
    step_alt = (end_alt - start_alt)/ numCoords

    coordList = []

    for i in range(0, numCoords):
        coordList.append((round(start_lat + (step_lat*i), 2), 
        round(start_lon + (step_lon*i),2), 
        round(start_alt + (step_alt*i),2)))
    
    return coordList

def transmit():
    import subprocess
    import time
    import shlex

    subprocess.call(shlex.split("dd if=Samples.iq8s of=Samples_256K.iq8s bs=4k seek=63"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.call(shlex.split("hackrf_transfer -t Samples_256K.iq8s -f 1240000000 -s 2000000 -x 45"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(1)
    

if __name__ == "__main__":

    from sys import argv, exit
    
    argc = len(argv)
    if argc != 9:
      print()
      print('Usage: '+ argv[0] +'  <ICAO> <Start Lat.> <Start Long.> <Start Alt.> <End Lat.> <End Long.> <End Alt.> <Speed (mph)>')
      print()
      print('    Example: '+ argv[0] +'  0xABCDEF 12.34 56.78 9999.0 43.21 87.65 99999.0 200')
      print()
      exit(2)

    icao = int(argv[1], 16)
    start_lat = float(argv[2])
    start_lon = float(argv[3])
    start_alt = float(argv[4])
    end_lat = float(argv[5])
    end_lon = float(argv[6])
    end_alt = float(argv[7])
    speed = float(argv[8])
    
    ca = 5
    tc = 11
    ss = 0
    nicsb = 0    
    time = 0       
    surface = False

    coordList = listCoords(start_lat, start_lon, start_alt, end_lat, end_lon, end_alt, speed)
    print("Number of Coords: ", len(coordList))
    for i in range(0, len(coordList), 1):
        lat = coordList[i][0]
        lon = coordList[i][1]
        alt = coordList[i][2]

        print("Lat: ", lat, ", Long: ", lon, ", Alt: ", alt)
        
        (df17_even, df17_odd) = df17_pos_rep_encode(ca, icao, tc, ss, nicsb, alt, time, lat, lon, surface)

        df17_array = frame_1090es_ppm_modulate(df17_even, df17_odd)

        samples_array = hackrf_raw_IQ_format(df17_array)

        SamplesFile = open("Samples.iq8s", "wb")

        SamplesFile.write(samples_array)

        transmit()


    