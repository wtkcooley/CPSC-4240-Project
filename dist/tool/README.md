# CPSC 4200 Final - System Monitor Tool

This tool expands on the functionality of psutil and it's ability to get system info from the os.
The tool gets info on the most memory intensive process and all of the network io devices. It displays this info in a GUI
and updates it every second as well as saves the first scan in a dated folder in the local project `logs` directory.

## Flags

* `-ng` / `--nogui` - Does not display GUI, just makes csv


## Usage

1. Install all required modules using the requirements file that is included. This can be done with the following command: `pip install -r requirements.txt`

2. Run: `python tool.py`

Note: If you get a permissions error your system may need to run the tool as a super user i.e. Run: `sudo python tool.py` instead

