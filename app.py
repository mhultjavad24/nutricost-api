from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/echo")
def echo():
    message = request.args.get("message", "")
    return {"message": message}

if __name__ == "__main__":
    app.run(debug=True)