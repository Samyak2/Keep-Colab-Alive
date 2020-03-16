# Keep Colab Alive

A selenium script to keep Google Colaboratory sessions running for longer and automate it (to some extent).

## Features

 - Keeps clicking on status indicator to keep colab alive
 - Executes given cells if not already running

## Requirements

 - Python 3 (testing with 3.7.5, should work with other python 3 versions)
 - selenium (see requirements.txt for version)
 - Firefox web browser

## Usage

Requires Python3 with selenium installed through pip. Run using `python3 keep_colab_alive.py`.

See `python3 keep_colab_alive.py --help` for the help page.

Arguments are taken through environment variables, if they are not set you will be prompted to enter them. Currently available arguments:
 - `FIREFOX_PROFILE`: The path to your Firefox profile through which you have logged in to Google. You can get the path by going to `about:profiles` in the Firefox URL bar. I suggest you create a new profile since a new profile starts up much faster than a bloated/old profile.
 - `COLAB_URL`: Link to the colab
 - `COLAB_CELLS`: Comma separated list of cell IDs to execute. (see below on how to get the IDs)

To the cell IDs, run the script with the `-c` flag like `python3 keep_colab_alive.py -c`. This will be show all the cells along with their IDs and some of the content.

Feel free to open an issue if there is any problem.

## TODO

 - [ ] Connect to runtime and execute all cells if runtime gets disconnected.
 - [x] More command line arguments
 - [x] Ask user input only in interactive mode

Open an issue if you want to suggest a feature.

