# ADS-B Out Implementation for 1240MHz for Testing

Written/Edited for python3

## Instructions
1. Execute *ADSB_Encoder.py* script with `<ICAO>` `<Latitude>` `<Longitude>` `<Altitude>` arguments:
```
$ ADSB_Encoder.py  0xABCDEF 12.34 56.78 9999.0
```
2. Make the raw signal file aligned to 256K buffer size:
```
$ dd if=Samples.iq8s of=Samples_256K.iq8s bs=4k seek=63
1+0 records in
1+0 records out
4096 bytes (4.1 kB) copied, 0.00110421 s, 3.7 MB/s
$
```
3. Transmit the signal into air:
```
$ hackrf_transfer -t Samples_256K.iq8s -f 868000000 -s 2000000 -x 10
```
## All-In-One
```
$ python3 errorplane.py  <ICAO> <Start Lat.> <Start Long.> <Start Alt.> <End Lat.> <End Long.> <End Alt.> <Speed (mph)>
```

Forked from lyusupov/ADSB-Out

