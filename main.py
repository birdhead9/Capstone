#webiste becomes a python package whenever an
#__init__.py file in inside a folder
from env import create_app

app = create_app()
#only if we run this file, then we
#will execute that line of the webserver
if __name__ == '__main__':
    app.run(debug=True)