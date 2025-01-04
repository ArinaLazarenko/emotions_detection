import json
from sklearn.discriminant_analysis import StandardScaler
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from datasets import load_dataset

# from transformers import BertTokenizer, BertModel
from sklearn.decomposition import PCA

_tokenizer = None
_model = None
_emotion_labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
_label_to_color = {
        'anger': 'black',
        'fear': 'purple',
        'sadness': 'blue',
        'surprise': 'green',
        'joy': 'orange',
        'love': 'red'
    }
_embeddings = []
_colors = []
_texts = []

def prepare_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained('bhadresh-savani/roberta-base-emotion')
        model = AutoModelForSequenceClassification.from_pretrained('bhadresh-savani/roberta-base-emotion')

        model.config.output_hidden_states = True

        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


def load_model():
    global _tokenizer, _model
    _tokenizer, _model = prepare_model()

# Define the prediction function
def predict_emotion(text):

    try:
        inputs = _tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        _model.eval()

        with torch.no_grad():
            outputs = _model(**inputs)
            logits = outputs.logits

        probabilities = torch.softmax(logits, dim=1).squeeze().tolist()

        predicted_class_idx = np.argmax(probabilities)

        predicted_emotion = _emotion_labels[predicted_class_idx]

        return predicted_emotion
    except Exception as e:
        print(f"Error during classification: {e}")
        return None

def example_data():
    # texts = [
    #     "I love you",
    #     "I hate you",
    #     "I am so sad",
    #     "I am so happy",
    #     "I am so scared",
    #     "I am so surprised"
    # ]
    dataset = load_dataset('emotion', split='test')
    texts = dataset['text']

    for text in texts:
        process_text(text, isExample=True)


def process_text(text, isExample=False):
    predicted_emotion = predict_emotion(text)
    add_embeddings(text)
    add_color(predicted_emotion)
    _texts.append((text, isExample))
    return predicted_emotion


def get_bert_embedding(text):
    inputs = _tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = _model(**inputs)
    hidden_states = outputs.hidden_states
    cls_embedding = hidden_states[-1][:, 0, :]
    return cls_embedding.detach().numpy()

def add_embeddings(text):
    # global _embeddings
    embeddings = get_bert_embedding(text)
    _embeddings.append(embeddings)

def add_color(emotion):
    # global _labels
    color = _label_to_color[emotion]
    _colors.append(color)




def pca():
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(np.vstack(_embeddings))
    return pca_result

def visualize():
    pca_result = pca()

    js_calls = "\n".join(
        f'addPoint({x}, {y}, "{color}", {json.dumps(text)}, "{"triangle" if index == len(pca_result) - 1 and not isExample else "point"}");'
        for index, ((x, y), color, (text, isExample)) in enumerate(zip(pca_result, _colors, _texts))
    )

    return js_calls


