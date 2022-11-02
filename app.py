from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['POST'])
def predict():
  return {'response': "HELLO!"}

if __name__ == "__main__":
  app.run()