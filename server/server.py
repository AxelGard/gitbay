from flask import Flask
from .models import TfIdf as Model
import json
from .models import score
from .models import tune 
from .models import util
from .models import config

app = Flask(__name__)
model = Model()
print("starting to train")
model.train()


@app.route("/")
def landing():
    return {"msg": "GitBay API"}


@app.get("/api/query/<q>")
def query(q):
    files = model.query(q)
    result = []
    for i, f in enumerate(files):
        cid = f.split("/")[-1]
        with open(f, "rb") as r_file:
            info = r_file.read()
            info = info.decode('utf-8', errors='ignore')
            if config.PARSE_HTML:
                info = util.clean([info])[0]
            else:
                info = util.clean_md([info])[0]
            info = info.replace("\n", " ").replace("  ", "")[:128] + " ..."
        pid = util.get_pid_from_cid(cid)
        result.append({"file": "ipfs://" + cid, "cid": cid, "pid":pid, "info": info, "meta_data": {}, "rank": i})
    return json.dumps(result)


@app.get("/api/model/score")
def get_score():
    scores = score.main()
    return json.dumps(scores)

@app.get("/api/model/tune/<model_name>")
def tune_model(model_name):
    scores = tune.main(model_name)
    return json.dumps(scores)
