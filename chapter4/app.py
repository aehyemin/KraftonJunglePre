from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True) # mac 은 5001, ctrl+c는 서버 종료