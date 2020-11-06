from flask import Flask
from client import main
import asyncio

app = Flask(__name__)

@app.route('/start-monitoring')
def start_monitoring():
    asyncio.get_event_loop().run_until_complete(main())
    return "good"

if __name__ == '__main__':
    app.run()