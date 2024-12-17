# Feasibility Study
This study documents all the potential challenges faced in the project and stratagies to overcome them and check if these features can be built be the team without compromising on the schedule. The strategy includes but is not limited to technology to be used, demo code and flowcharts. This study is not about the exact approach to building the software rather than highlighting whether the most challenging features can be implemented by the team.

## What summarization model to use ?

### Challenges
We need to create / fine tune a Large Language Model for summarization task. One what metrics to evaluate this model ? The team has no experience with LLMs. How do we fine tune the model ? How do we get the data for fine tuning the model ? How to fit bullet points in the summary to correct classes that model may not be previously aware of ? The need to fine tune the model is that most summarization models are about providing a bird's eye view or a gist and missing out on details but here the objective is to reduce redundancies in the emails. The summary must not miss out on any details.

### Proposed strategy
* Evaluation metrics to be used are:
1. Summarization
**Primary Metric**: Use **ROUGE-1** and **ROUGE-2** for quantitative evaluation of content inclusion and coherence.
**Secondary Metric**: Use **ROUGE-L** for evaluating how well the summary maintains the logical flow of ideas.

2. Categorization
Accuracy, Precision, Recall and F1 score	
* Models and libraries to be used
1. **Models**:
    
    -   **Longformer**: Handles long inputs with high token counts.
    -   **PEGASUS**: Pretrained for summarization, supports abstractive summarization.
    -   **BART**: Effective for multi-document summarization when fine-tuned.
   
2. **Libraries**:
    
    -   **Hugging Face Transformers**: For pretrained summarization models.
    -   **spaCy / scikit-learn**: For clustering and text preprocessing.
    -   **Sumy / Gensim**: For extractive summarization.
* Dataset to use for fine tuning the model
* 
	Email thread summarization : https://www.kaggle.com/datasets/marawanxmamdouh/email-thread-summary-dataset
	
	Multi news summarization :
	https://www.kaggle.com/datasets/sbhatti/news-summarization

* Reducing Redundancy
Preprocessing the data by removing very similar emails using the cosine similarrity based on their word embeddings derived from pre-trained models like Word2Vec.

## How to create portable backend ?

### Challenges

We need to setup our backend server as well as the entire AI model on user's servers. Changing the backend server will most likely involve changing the API endpoint. How do we do this without redeplying the entire website ? (that is cause the frontend to use a different API point dynamically ) The user must not be able to access the source code of our backend or AI model.

### Proposed Strategy for Portable Backend

1. **Dynamic API Endpoint Management:**

Use a config.json file or environment variables to dynamically fetch the API endpoint in the frontend.

2. **Containerized Deployment:**

Package the backend and AI model into a Docker container.

3. **Code and Model Security:**

Encrypt AI model files and decrypt them at runtime inside the container.

4. **Seamless Updates:**

Host Docker images on a centralized registry.

5. **User Documentation:**

Provide a clear guide with setup steps and API key management.


## How to get access to user's emails ?

### Challenges

We need to be able to read user's emails and the software must accept emails of from a variety of email services (gmail, outlook) etc. We not only the email content but also the date and time when it was sent, who was the sender as well as people it was forwarded to. Can we access what type of attachment is there in the email ?

### Proposed strategy

Gmail API or Microsoft Graph APIs can be used for this.
