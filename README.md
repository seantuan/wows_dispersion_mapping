# WoWs Dispersion Mapping

***WiP***

This is a program writen in Python for mapping shell dispersion in World of Warships using topdown-veiw videos recorded from replays.

### Dependencies
```
numpy, scipy, filterpy, matplotlib, opencv
```

## How to use

This program consists of 4 python scripts, `read_video.py`, `process_data.py`, `plot.py`, `evaluate.py`. 

`read_video.py` will read the input video and genernate raw data of coordinates of shell landing points stored in json file with a same name as input video. Also, it will calibrate the data by the length of Fuso in the video and the angle of trajectories of shells. The calibrated data will be stroed in both json and csv files with a suffix "_calibrated".

`process_data.py` provides a stand-alone way to calibrate the raw data.

`plot.py` will read the calibrated data in json file and generate the horizontal and vertical histograms and the scatter plot.

`evaluate.py` will read the testing dataset consisted of video clips and corresponding csv files to evaluate the mapping errors.

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

To run the evaluation program:

```
python evaluate.py -d <path-to-testing-data-folder>
```

or

```
evaluate.exe -j <path-to-testing-data-folder>
```

## How to set up video recording

1. Set WoWs graphic setting to `Low`.
2. Put the provided mods to `<World_of_Warships>/res_mods/<version>/`.
3. Set up the recording program with the output of 1280x720, 60 fps and reasonable bit rate.
4. Open the replay, use `Ctrl + Shift + Backspace + r` to enter free cam, use the number keys to navigate and set up a top-down view over the target area, just like the example provided.
5. Start recording in 1/2 speed by pressing `delete` once, please make sure there's no shots entering the FoV during the start and the end of the recorded video.
6. Have fun while waiting! O3O

## Todo list
* Limit the number of mapped points drawn on the screen during processing in order to accelerate the processing speed.
* Find solutions for mis-detections

=w=
