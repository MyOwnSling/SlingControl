
# What is this?
SlingControl is mostly a generic python3 task runner intended as a learning exercise in dynamically-loaded python modules that are used to drive a basic home automation/status display center, all running on a Raspberri Pi Zero (W).
## Modules Types
These module types correspond to the three directories under **src**.
- modules - core logic modules intended to gather/send desired data (e.g. get the weather, check the network, turn smart lights on/off)
- notifiers - notifier modules intended to take alerts generated by core modules and perform the associated notifications (e.g. send SNS messages in AWS, push a Pushbullet notification)
- dashboards - dashboard modules intended to display data passed from core modules (e.g. Tipboard)
## My Implementation
I chose Tipboard and Pushbullet for my dashboard and notification utilities, so there is code and config specific to those in this repo. Pushbullet is free and doesn't use SMS. Tipboard is relatively simple and light, though it is no longer maintained and is built on python2 which is now out of support. Since I am choosing to run on a Raspberry Pi Zero (W), I chose to use Alpine for my Docker image due to how light it is. These selections could be switched for others, though the Dockerfile would have to be tweak to a certain extent and entire modules would need to be written for different notifiers and dashboards. In the future, I would like to add templating or something similar to make it easier to get started with different options.
### Tipboard
Tipboard is a python2-based dashboard with HTLM/javascript for the frontend and a Redis database used in the backend. It takes simple API calls to its webserver for updating and configuring tiles defined in a static config file.
### Raspberry Pi Zero
In order to get the Docker image to run on a Rasperry Pi Zero (running Raspbian, though the OS may not matter), I had to use an older version of Alpine (3.8).

# Requirements
These are requirements for getting a container built and running usingthe **run-container** script.
## Docker
All application code and supporting software are intended to be installed inside of a Docker image.
## keepassxc 
Keepassxc is used to securely store secrets such as passwords, API keys, etc. Required secrets must be populated in an associated Keepass database.

# Getting Started
**Note:** the included core modules are empty and will do nothing out of the box; you will have to write something first.
1. cd SlingControl/docker
2. Run **./run-container <path to keepass database (kdbx file)> -c** and enter database password when prompted
3. Wait for the build to complete; the container will start running afterward (omit the **-c** from the above command to run without rebuilding)
4. Open browser to **localhost:7272** and wait a minute or so for Tipboard to start updating the dashboard values
