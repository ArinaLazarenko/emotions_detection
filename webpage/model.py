import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from safetensors.torch import load_file

tokenizer = None
model = None
emotion_labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def prepare_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained('bhadresh-savani/roberta-base-emotion')
        model = AutoModelForSequenceClassification.from_pretrained('bhadresh-savani/roberta-base-emotion')

        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


def load_model():
    global tokenizer, model
    tokenizer, model = prepare_model()


# Define the prediction function
def predict_emotion(text):

    if tokenizer is None or model is None:
        print("Failed to load the model.")
        exit(1)

    inputs = tokenizer(text, return_tensors='pt')
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return emotion_labels[predicted_class]


