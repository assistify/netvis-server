# NetVis Server

A Node.js application for a
[NetVis](https://github.com/jschirrmacher/netvis.git) based frontend
together with some sample data to provide an example for a quick start
for own implementations.

## What can it do?

- Display different types of network relations between nodes.
- Show detail descriptions for each node (if supplied) by clicking on the node.
- Optimized for larger networks by showing related nodes only when requested.
- Live-Edit feature: when changing the details of a node, those changes are sent to other clients via Websocket in real-time.
- View-only version (without edit feature) works without a backend on every simple web server just by copying the files.



## Install and start server

If you do not want to use docker, or if you want to have more control over the code,
you should install [Node.js](https://nodejs.org/en/) at least in version 8 and checkout the code.

Install the server with

    git clone https://github.com/jschirrmacher/netvis-server.git

After that, install all dependencies:

    npm install

then start the server:

    npm start

or, if you want to change the code, the development server, which
watches the source files and restarts when a change is recognized:

    npm run start-dev

Then open http://localhost:3000 and see the example data in your browser

## Parameters

If port 3000 is already occupied on your machine, or if you just like to
use another port, simply set the environment before starting the server:

    PORT=3001 npm start
