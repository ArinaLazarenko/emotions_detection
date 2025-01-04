from flask import Flask, request, render_template
import model as m

app = Flask(__name__)

# Route to display the homepage
@app.route('/')
def index():
    js_calls = m.visualize()
    return render_template('index.html', js_calls=js_calls)

# Route to handle text submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    emotion = m.process_text(text)
    js_calls = m.visualize()
    return render_template('index.html', text=text, emotion=emotion, js_calls=js_calls)

if __name__ == '__main__':
    m.load_model()
    m.example_data()
    app.run(debug=True)

