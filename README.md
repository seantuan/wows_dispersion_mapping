# WoWs Dispersion Mapping

WiP

This is a program writen in Python for mapping shell dispersion in World of Warships using topdown-veiw videos recorded from replays.

### Dependencies
```
numpy, scipy, filterpy, matplotlib, opencv
```

### How to use

This program consists of 3 python scripts, `read_video.py`, `process_data.py`, `plot.py`. 

`read_video.py` will read the input video and genernate raw data of coordinates of shell landing points stored in json file with a same name as input video. Also, it will calibrate the data by the length of Fuso in the video and the angle of trajectories of shells. The calibrated data will be stroed in both json and csv files with a suffix "_calibrated".

`process_data.py` provides a stand-alone way to calibrate the raw data.

`plot.py` will read the calibrated data in json file and generate the horizontal and vertical histograms and the scatter plot.

To run the program, type:

```
python read_video.py -v <path-to-video>
```

or

```
read_video.exe -v <path-to-video>
```

Then type:

```
python plot.py -j <path-to-calibrated-json-file>
```

or

```
plot.exe -j <path-to-calibrated-json-file>
```
