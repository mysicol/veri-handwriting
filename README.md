# VeriHandwriting

<img src="/documentation/index.png" width="1000">
<img src="/documentation/upload_image.gif" width="1000">
<img src="/documentation/statistics_page.png" width="1000">


![Input animation](/documentation/index.png)
![Results animation](/documentation/upload_image.gif)
![Results screenshot](/documentation/statistics_page.png)

### Authentication keys

You must have a valid authentication key for the OpenAI API. Store it in a file called `back/.env` in the following format:

`OPENAI_API_KEY="your_openai_key"`

### Running on Windows

In a terminal, run:

`python -m venv .venv` (only do the very first time to create venv)

`.venv/Scripts/activate`

`pip install -r requirements.txt`

`cd back`

`python server.py` <br><br>

In another terminal, run:

`cd front/`

`npm i`

`npm run dev`

Visit the localhost address generated to view the program.

### Running on Mac

In a terminal, run:

`python3 -m venv .venv` (only do the very first time to create venv)

`source .venv/bin/activate`

`pip3 install -r requirements.txt`

`cd back`

`python3 server.py` <br><br>

In another terminal, run:

`cd front/`

`npm i` 

`npm run dev` <br>

Visit the localhost address generated to view the program.

## Authors
Francisco Cruz-Urbanc, fjc59@drexel.edu

William Dorman

Abigail Hatcher, ah3658@drexel.edu

Charlie Meader

Adam Steppe