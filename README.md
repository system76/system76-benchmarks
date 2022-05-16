# system76-benchmarks

Collection of benchmarking tools developed by System76

## Battery

Used to quickly test battery longevity under various loads and profiles. 

### Usage

```
benchmark.py -h
usage: benchmark.py [-h] [--info] [--quick] [--monitor] [--test TEST]
options:
 -h, --help   Show this help message and exit
 --info       Gather and display battery info
 --quick      Run a quick battery test
 --full       Run comprehensive battery test
 --monitor    Monitor battery in 5 second intervals
 --test TEST  Run selected test (examples found in ./tests)
```

#### --full

Runs 5 minute tests cycling through power profiles and brightness levels. Outputs to stdout



#### --quick

Runs 2 minute tests cycling through power profiles at 50% brightness



#### --info

Prints current info about the battery and power profile to stdout



#### --monitor

Prints info about the battery every 5 seconds until killed. 



#### --test

Uses json formatted file to create custom tests. 



### Custom Test creation

Below is an example test file found in the `test` folder within the benchmark. 

```json
{
"name": "Heavy Load", 
"backlight": 0.5,
"profile": "balanced",
"duration": 10,
"apps": [["firefox","https://www.youtube.com/watch?v=bem_d49NBLc"],
 ["steam"],["nautilus"],["libreoffice"],["io.elementary.appcenter"],
 ["flatpak","run","com.visualstudio.code"]
 ]
}
```
