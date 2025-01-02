from flask import Flask, request, render_template
import model as m

app = Flask(__name__)

# Route to display the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle text submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    emotion = m.predict_emotion(text)
    return render_template('index.html', text=text, emotion=emotion)

if __name__ == '__main__':
    m.load_model()
    app.run(debug=True)

