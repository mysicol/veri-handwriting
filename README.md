# WriteRight

### Philly Codefest, March 2025 at Drexel University

## Overview

WriteRight is a tool that utilizes machine learning and artificial intelligence to assist users in improving their handwriting skills! Given a handwritten sample, WriteRight identifies characters and compiles a report including spelling and grammar feedback as well as suggestions for particular characters to focus on writing more neatly.

WriteRight is intended for use by children learning to write and by foreign learners practicing written English. We hope to improve and automate the process of learning any written language, with the goal of extending our technology to identify non-English characters in the future.

<img src="/documentation/index.png" width="1000">
<img src="/documentation/upload_image.gif" width="1000">
<img src="/documentation/statistics_page.png" width="1000">

## Description

This application is written in Python and React. When an image is uploaded, it is split into a grid of squares using OpenCV, and the character in each square is identified using the EasyOCR text recognition model. Then the images are assigned a neatness percentage using our trained linear regression model. Finally, these statistics are compiled in a report and the OpenAI API is used to provide supplementary verbal feedback.

## Running WriteRight

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