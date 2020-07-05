# ADS-B Out Implementation for 1240MHz for Testing

Written/Edited for python3

## Instructions
1. Execute *ADSB_Encoder.py* script with `<ICAO>` `<Latitude>` `<Longitude>` `<Altitude>` arguments:
```
$ ADSB_Encoder.py  0xABCDEF 12.34 56.78 9999.0
$ ls Samples.iq8s
Samples.iq8s
$
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
call hackrf_sample_rate_set(2000000 Hz/2.000 MHz)
call hackrf_baseband_filter_bandwidth_set(1750000 Hz/1.750 MHz)
call hackrf_set_freq(868000000 Hz/868.000 MHz)
Stop with Ctrl-C
 0.5 MiB / 1.000 sec =  0.5 MiB/second

User cancel, exiting...
Total time: 1.00038 s
hackrf_stop_tx() done
hackrf_close() done
hackrf_exit() done
fclose(fd) done
exit
$
```
## All-In-One

python3 errorplane.py  <ICAO> <Start Lat.> <Start Long.> <Start Alt.> <End Lat.> <End Long.> <End Alt.> <Speed (mph)>


