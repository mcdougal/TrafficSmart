[README]

[TEAM]
  1. Team name: iAI
  2. Team members:
    - Cedric McDougal
	- Wei Dai
	- Shashikanth Sreenivasaiah
	- Taylor Johndrew

[ENVIRONMENT]
  1. Python 2.7
  2. Chrome, Firefox, Safari, IE 9 or newer 

[ABOUT TrafficSmart]
  1. Python to implement the algorithm
  2. JavaScript and HTML5 to show the result in browsers

[HOW TO RUN]
  1. cd to top level directory folder (contains run.py)
  
  2. Execute the run.py file like this:
    
    ./run.py [-h] [-b BREAKPOINT] [-v] [-d] data_file agent_file
    
    Mandatory arguments:
        data_file            JSON file containing intersection definitions, can be found in ./tests folder
        agent_file           Python file with AI Agent class to change lights, can be found in ./ai folder
    Optional arguments:
        -h, --help           show this help message and exit
        -v, --verbose        print out debug info
        -d, --draw           dump data.js
        -b BREAKPOINT        pause execution at this frame and enter debug mode
  
  3. To view the result in HTML5, use ‘-d’ then open ui/ui.html use browser.
     UI Shortcut keys:
        o                    previous frame
        p                    next frame
        k                    previous cycle
        l                    next light cycle
        n                    first frame
        m                    last frame
        spacebar             play/pause
        [                    reduce delay
        ]                    increase delay
        j                    jump to frame

[EXAMPLES]
  1. To run the program using 2*2 map and use a random agent:
    ./run.py tests/2x2.json ai/random.py
  
  2. To run the a 3*3 map using a simple agent and use html5 to see the result:
    ./run.py -d tests/3x3.json ai/simple.py
    then open ui/ui.html
