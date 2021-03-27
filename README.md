# ESD-project

## Installation: Back end
### Setting up a virtual environment
If you have not set up your virtual environment, it is recommended that you do so. If not, install the modules used in this project at your own risk!
A virtual environment allows dependencies to be separated between projects. As the dependency modules are updated, conflicts can arise between projects if dependencies are shared and the necessary versions are not the same. A virtual environment eliminates these conflicts by allowing the dependencies to be project specific and isolated from the system.
```bash
cd server
python -m venv venv
```
This creates a fresh virtual environment called "venv", located in ESD-project/server.

### Activate virtual environment
Before running the Flask apps, you first have to activate the virtual environment, like so:

Windows
```bash
cd server
venv\Scripts\activate
```

UNIX bash
```bash
cd server
venv/bin/activate
```
This prevents any conflicts between the Python packages used in this project and the packages in your local machine.

### Install packages
Then install the required Python packages.
```bash
pip install -r requirements.txt
```

### Running the Flask Apps
Run Flask Apps with
```bash
python filename.py
```

### Running roomManagement.py
If you fail to run roomManagement.py, we have to set the environment variable FLASK_APP within our virtual environment.

Add this line of code at the end of <code>venv/bin/activate</code> if you are using a UNIX system. 
```bash
export FLASK_APP=roomManagement
```

For Windows, in <code>venv\Scripts\activate.bat</code>.
```batch
set FLASK_APP=roomManagement
```

Then run the app.
```bash
python roomManagement.py
```

### Setting up RabbitMQ Docker and Tele Bot logging
Ensure that your docker is up and running and that your containers created from Lab 6 / Lab 10 are either stopped or deleted

Run this line of code in your terminal:
```
docker run -d --hostname esd-rabbit --name proj-rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Then navigate into the server folder and run this file to set up exchange and queues:
```
cd server
python amqp_setup.py
```

Finally, run the development server, app.py/roomManagement.py, activity_log.py, error_log.py on 4 different terminals in their respective directories.

## Installation: Front end
### Have node.js installed
Make sure that you have node.js installed on your machine.
https://nodejs.org/en/download/

Node.js will run the Vue app on the node.js server for development. We will also use it to manage packages.
### Install packages
Install the packages with this command.
```bash
cd client
npm install
```

### Run a development server with hot-reloading
```bash
npm run serve
```

