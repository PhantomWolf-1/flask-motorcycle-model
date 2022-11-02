from flask import Flask, request

app = Flask(__name__)


#response
@app.route("/", method=["POST"])
def response():

    #query = dict(request.form)['query']
    #result = query + " " + time.ctime()
    return {'response' : "HELLO"}


@app.before_request
def only_json():
    if not request.is_json:
        abort(400)

        
#if __name__ == "__main__":
#   app.run(host="0.0.0.0",)