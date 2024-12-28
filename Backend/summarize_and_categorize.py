from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize the model and tokenizer globally
MODEL = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
TOKENIZER = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize the model and tokenizer globally
MODEL = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
TOKENIZER = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

def generate_summary(emails, max_token_limit=1024):
    # Add an introductory prompt to guide the model (optional)
    base_prompt = "Summarize the following emails without skipping any important information."

    email_content = ""
    for email_info in emails:
        email_content += f"from: {email_info['from']} content: {email_info['snippet']} "

    base_prompt += email_content

    # Tokenize the base prompt to check token count
    inputs = TOKENIZER(base_prompt, return_tensors="pt", truncation=False)
    input_length = inputs['input_ids'].shape[1]

    # Check if the input exceeds the max token limit
    if input_length > max_token_limit:
        # Split the input into chunks if it exceeds the token limit
        chunks = []
        start_idx = 0

        # Split into smaller chunks, ensuring each chunk does not exceed the token limit
        while start_idx < input_length:
            end_idx = min(start_idx + max_token_limit - 1, input_length)
            chunk = base_prompt[start_idx:end_idx]
            chunks.append(chunk)
            start_idx = end_idx
        
        # Generate a summary for each chunk and combine them
        summaries = []
        for chunk in chunks:
            inputs = TOKENIZER(chunk, return_tensors="pt")
            summary_ids = MODEL.generate(inputs['input_ids'], max_length=150, num_beams=5, early_stopping=True)
            generated_summary = TOKENIZER.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(generated_summary)
        
        # Combine summaries from all chunks
        final_summary = " ".join(summaries)
    else:
        # If input length is within the limit, generate the summary directly
        inputs = TOKENIZER(base_prompt, return_tensors="pt")
        summary_ids = MODEL.generate(inputs['input_ids'], max_length=150, num_beams=5, early_stopping=True)
        final_summary = TOKENIZER.decode(summary_ids[0], skip_special_tokens=True)

    # Post-processing to remove the introductory phrase if it's present
    intro_phrase = "Summarize the following emails without skipping any important information."
    if final_summary.startswith(intro_phrase):
        final_summary = final_summary[len(intro_phrase):].strip()

    return final_summary
