# VeriHandwriting

### Authentication keys

You must have a valid authentication keys for OpenAI API to run. Store it in a file called `back/.env` in the following format:

`OPENAI_API_KEY="your_openai_key"`

### Running on Windows

In a terminal, run:

`cd back/`

`python -m venv venv` (only do the very first time to create venv)

`venv/Scripts/activate`

`pip install -r requirements.txt`

`python server.py` <br><br>

In another terminal, run:

`cd front/`

`npm i`

`npm run dev`

Visit the localhost address generated to view the program.

### Running on Mac

In a terminal, run:

`cd back/`

`python3 -m venv venv` (only do the very first time to create venv)

`source venv/bin/activate`

`pip3 install -r requirements.txt`

`python3 server.py` <br><br>

In another terminal, run:

`cd front/`

`npm i` 

`npm run dev` <br>

Visit the localhost address generated to view the program.