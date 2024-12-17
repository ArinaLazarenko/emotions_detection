from flask import Flask, request, render_template
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from safetensors.torch import load_file

# Initialize Flask app
app = Flask(__name__)

# # Function to load the model with error handling
# def load_model():
#     try:
#         # Load the tokenizer and model
#         tokenizer = RobertaTokenizer.from_pretrained('model/results/checkpoint-4000')
#         model = RobertaForSequenceClassification.from_pretrained('model/results/checkpoint-4000')
#         return tokenizer, model
#     except Exception as e:
#         print(f"Error loading model: {e}")
#         return None, None
    
# # C:\Users\arian\OneDrive\Робочий стіл\lab emotions\model\results\checkpoint-4000
# # model\results\checkpoint-4000

def load_model():
    try:
        # Шляхи до файлів
        model_path = 'C:/Users/arian/OneDrive/Робочий стіл/lab emotions/model/results'
        config_path = f"{model_path}/config.json"
        model_weights_path = f"{model_path}/model.safetensors"

        # Завантаження токенізатора
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

        # Завантаження ваг у форматі safetensors
        state_dict = load_file(model_weights_path)

        # Завантаження моделі
        model = RobertaForSequenceClassification.from_pretrained(
            model_path,
            config=config_path,
            state_dict=state_dict,
        )



        # # Load the tokenizer normally
        # tokenizer = RobertaTokenizer.from_pretrained('C:/Users/arian/OneDrive/Робочий стіл/lab emotions/model/results/checkpoint-4000')
        
        # # Load the model manually if necessary
        # model = RobertaForSequenceClassification.from_pretrained(None, config='C:/Users/arian/OneDrive/Робочий стіл/lab emotions/model/results/checkpoint-4000/config.json')
        # model_state = torch.load('C:/Users/arian/OneDrive/Робочий стіл/lab emotions/model/results/checkpoint-4000/model.safetensor')
        # model.load_state_dict(model_state)
        
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


# Load model and tokenizer
tokenizer, model = load_model()

# Check if the model was successfully loaded
if tokenizer is None or model is None:
    print("Failed to load the model.")
    exit(1)

# Emotion labels corresponding to your model output
emotion_labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

# Define the prediction function
def predict_emotion(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1).item()
    return emotion_labels[predicted_class]

# Route to display the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle text submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    emotion = predict_emotion(text)
    return render_template('index.html', text=text, emotion=emotion)

if __name__ == '__main__':
    app.run(debug=True)

