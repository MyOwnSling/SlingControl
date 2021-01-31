
# Requirements
- Docker
- keepassxc **(Required passwords must be popluated in a keepass database)**

# Getting Started
1. cd SlingControl/docker
2. Run **./run-container <path to keepass database (kdbx file)> -c** and enter database password when prompted
3. Wait for the build to complete; the container will start running afterward (omit the **-c** from the above command to run without rebuilding)
4. Open browser to **localhost:7272** and wait a minute or so for Tipboard to start updating the dashboard values
