from sanic import Sanic, response
from Scheduler import Scheduler
import datetime
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app)


@app.route("/")
async def index(request):
    return response.text("/api")


@app.route("/api")
async def api(request):
    # set date to 20 minutes from now
    now = datetime.datetime.now() + datetime.timedelta(minutes=27)
    time = Scheduler().get_info(now)
    return response.json(
        {
            "current_time": str(now),
            "period": time.period,
            "day_type": time.day_type,
            "time_left": str(time.time_left),
            "time_left_in_seconds": time.time_left.seconds,
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)