from collections import defaultdict
from transformers import BartForSequenceClassification, BartTokenizer
import torch

# Load the BART MNLI model and tokenizer
MODEL_NAME = 'facebook/bart-large-mnli'
MODEL = BartForSequenceClassification.from_pretrained(MODEL_NAME)
TOKENIZER = BartTokenizer.from_pretrained(MODEL_NAME)

def categorize_label_wise(classifications : list[dict]):
    label_and_contents = defaultdict(list)
    for classification in classifications:
        label = classification["label"]
        content = classification["content"]
        label_and_contents[label].append(content)
    return label_and_contents
            

def classify_emails(emails, possible_labels, hypothesis_template="This email is about {}."):
    """
    Classify emails according to their content using zero-shot classification with BART.

    Parameters:
    - emails (list of str): List of email content to classify.
    - possible_labels (list of str): List of potential categories for classification.
    - hypothesis_template (str): Template for generating hypotheses for classification.

    Returns:
    - list: list of dictionary with email and associated label and scores fields.
    """
    classifications = []
    
    for email in emails:
        # Prepare input pairs for each label
        inputs = []
        for label in possible_labels:
            hypothesis = hypothesis_template.format(label)
            inputs.append((email, hypothesis))
        
        # Tokenize inputs
        tokenized_inputs = TOKENIZER(
            [pair[0] for pair in inputs],  # Premises (email content)
            [pair[1] for pair in inputs],  # Hypotheses
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        
        # Perform inference
        with torch.no_grad():
            outputs = MODEL(**tokenized_inputs)
            logits = outputs.logits  # [batch_size, 3] for entailment, neutral, contradiction
            entailment_scores = logits[:, 2]  # Index 2 corresponds to entailment
        
        # Identify the label with the highest entailment score
        scores = torch.softmax(entailment_scores, dim=0).tolist()
        best_label_idx = torch.argmax(entailment_scores).item()
        classification = {
            "content" : email,
            "label": possible_labels[best_label_idx]
        }
        classifications.append(classification)

    return categorize_label_wise(classifications)
