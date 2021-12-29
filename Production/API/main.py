from sanic import Sanic, response
from Scheduler.Scheduler import Scheduler
import datetime
from sanic_cors import CORS
app = Sanic(__name__)
CORS(app)

@app.route("/")
async def index(request):
	return response.redirect("/api")


@app.route("/api")
async def api(request):
	now = datetime.datetime.now() - datetime.timedelta(hours=5)
	print(now)
	time = Scheduler().get_period_info(now)
	return response.json(time.json())


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)
