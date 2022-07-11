
Most part of the code in search.py and scholar.py is adopted from https://github.com/michael-act/Senginta.py



## Disclaimer: 
This code is for educational purposes only and the user is responsibe for any usage of the code.

## Installation:
1. Install the requiements in requirements.txt
2. If want to manually install browser driver see see macos_chrom_install_manual.txt and set driver_path in getwebpage.py


## Usage:
1. Set keywords and first_page and last_page  in run_gscholar.py
1. Run the scholar searcher : python run_gscholar.py
3. It stores a .json file and a csv.file that hold the extracted papers.
 


v1:
-That code does not run anymore because google recognizes the robot and blocks it. 
I replaced it with a code that goes around this problem using google chrom driver.
-automated installation of chromdriver


v2 : 
debugged for entries that have no url
output is saved both as json and csv files
added docker_file 

