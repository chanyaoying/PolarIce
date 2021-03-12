# ESD-project

## Running the Backend
### Activate virtual environment
Before running the Flask apps, you first have to activate the virtual environment, like so:
```bash
virtualenv\Scripts\activate
```
This prevents any conflicts between the Python packages used in this project and the packages in your local machine.

### Install packages
Then install the required Python packages.
```bash
cd server
pip install -r requirements.txt
```

### Running the Flask Apps
Run Flask Apps with
```bash
python filename.py
```

If you fail to run roomManagement.py, run these commands to set the environment variable FLASK_APP:
```bash
set FLASK_APP=roomManagement
```

For macOS, Linux users:
```bash
export FLASK_APP=roomManagement
```

Then run the app.
```bash
python roomManagement.py
```

## Running the Frontend
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

