from sanic import Sanic, response
from Scheduler.Scheduler import Scheduler
import datetime
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app)


@app.route("/")
async def index(request):
    return response.text("/api")


@app.route("/api")
async def api(request):
    now = datetime.datetime.now() + datetime.timedelta(minutes=5+18, seconds=10)
    time = Scheduler().get_period_info(now)
    return response.json(time.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
