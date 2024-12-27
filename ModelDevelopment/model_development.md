# LLM Model Development

This document outlines all experiments conducted by the team to develop or fine-tune the model. It includes references used during research, the utilization of cloud services, and the machine learning pipelines employed.

## Experiment One: Fine-Tuning the BART Model

### Dataset

The dataset used for this experiment is available at:  
[Email Thread Summary Dataset](https://www.kaggle.com/datasets/marawanxmamdouh/email-thread-summary-dataset)

### Model

The BART-large model from Hugging Face's Transformers library was selected for fine-tuning. The Transformers library was utilized exclusively for pipeline development.

### Cloud Services

AWS SageMaker Studio was employed for this experiment, leveraging its Jupyter Space and Training Jobs features.

-   **AWS SageMaker Jupyter Space**: This feature provides an interactive environment to write and execute Python code. It allows users to develop and test scripts in a managed Jupyter Notebook environment without the need to set up or manage computing instances manually.
-   **Training Jobs**: AWS SageMaker Training Jobs enable programmatic execution of training tasks on specified hardware configurations, handling instance provisioning and management automatically.

In this experiment, the team used the Jupyter Space to write and execute code that programmatically set up a SageMaker Training Job. This approach facilitated efficient training of the model without concerns about instance management.

Details of the services used are as follows:

-   **Training Job**: `arn:aws:sagemaker:us-east-1:767398072245:training-job/pytorch-training-2024-12-27-14-32-37-754`
-   **SageMaker Domain**: `d-ht7zbmtb77d9`
-   **SageMaker User Profile**: `arn:aws:iam::767398072245:role/service-role/AmazonSageMaker-ExecutionRole-20241224T012277`
-   **SageMaker Studio**: `studio-d-ht7zbmtb77d9.studio.us-east-1.sagemaker.aws`

### Failed Approaches

Fine-tuning the BART model presented several challenges. Below is a summary of the unsuccessful attempts to avoid repetition of inefficiencies:

1.  **Fine-Tuning on a Local Machine**
    
    -   Continuous power and monitoring were required.
    -   The process was time-intensive, causing the machine to overheat.
    -   CPU usage consistently reached 100%, posing a risk of long-term hardware damage.
    -   Fine-tuning on a local machine was abandoned due to these constraints.
2.  **Fine-Tuning Using an AWS EC2 Instance**
    
    -   Cost minimization was a priority for the team.
    -   Free-tier EC2 instances, typically equipped with only two CPU cores, were inadequate for the fine-tuning process.
    -   The Jupyter notebook kernel frequently crashed.
    -   This approach was deemed impractical and was set aside in favor of exploring more cost-effective alternatives.
3.  **Fine-Tuning Using an AWS SageMaker Studio Notebook Instance**
    
    -   AWS SageMaker Studio provides Jupyter notebook environments with access to high-end CPUs (e.g., 8 cores).
    -   However, uninterrupted browser connectivity and consistent internet access were required for the duration of the fine-tuning process.
    -   Despite implementing checkpointing after each epoch, the average runtime for one epoch was approximately 16 hours.
    -   Due to the challenges in ensuring continuous connectivity, this approach was discontinued.