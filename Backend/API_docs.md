
# Email Processing API Documentation

This document outlines the APIs provided by the email processing service. These APIs allow users to authenticate via Google OAuth, read emails, and retrieve classified summaries. Authentication is handled via OAuth 2.0, and MongoDB is used for data storage.

## Base URL

`http://localhost:5000`


## **1. `/authorize`**

### Description
Initiates the Google OAuth 2.0 flow for user authentication.

### Method
`GET`

### Request
No request body required.

### Response
Redirects the user to Google's OAuth authorization page.

---

## **2. `/callback`**

### Description
Handles the callback from Google after user authentication and stores credentials in the session.

### Method
`GET`

### Request
No request body required. Google will append authentication details in the query parameters.

### Response
Redirects the user to the `/read_emails` route after successful authentication.

---

## **3. `/logout`**

### Description
Logs the user out by clearing the session.

### Method
`GET`

### Request
No request body required.

### Response
Redirects the user to the `/authorize` route.

---

## **4. `/read_emails`**

### Description
Retrieves emails from the user's Gmail inbox for a specific date.

### Method
`POST`

### Request
#### Headers
- `Content-Type: application/json`

#### Body
```json
{
    "target_date": "YYYY-MM-DD"
}
```

### Response
#### Success (200)
```json
[
    {
        "id": "12345",
        "snippet": "Email snippet",
        "from": "sender@example.com",
        "time": "Mon, 30 Dec 2024 12:34:56 +0000"
    },
    ...
]
```

#### Error (401 - User not authenticated)
Redirects to `/authorize`.

#### Error (500 - Other issues)
```json
{
    "error": "Error message"
}
```

---

## **5. `/get_classified_summary`**

### Description
Generates summaries of emails and classifies them into predefined categories.

### Method
`POST`

### Request
#### Headers
- `Content-Type: application/json`

#### Body
```json
{
    "target_date": "YYYY-MM-DD",
    "categories": ["Category1", "Category2", "Category3"]
}
```

### Response
#### Success (200)
```json
{
    "classified_summaries": {
        "Category1": ["Summary1", "Summary2"],
        "Category2": ["Summary3"],
        "Category3": []
    }
}
```

#### Error (401 - User not authenticated)
Redirects to `/authorize`.

#### Error (500 - Other issues)
```json
{
    "error": "Error message"
}
```


## Error Handling

### General Errors
- **401 Unauthorized**: Redirects to `/authorize` if the user is not authenticated.
- **500 Internal Server Error**: Returns an error message for all other issues.


## Examples

### 1. Reading Emails
#### Request
```bash
curl -X POST http://localhost:5000/read_emails \
-H "Content-Type: application/json" \
-d '{"target_date": "2024-12-30"}'
```

#### Response
```json
[
    {
        "id": "12345",
        "snippet": "Email snippet",
        "from": "sender@example.com",
        "time": "Mon, 30 Dec 2024 12:34:56 +0000"
    }
]
```


### 2. Getting Classified Summary
#### Request
```bash
curl -X POST http://localhost:5000/get_classified_summary \
-H "Content-Type: application/json" \
-d '{
    "target_date": "2024-12-30",
    "categories": ["Work", "Personal", "Spam"]
}'
```

#### Response
```json
{
    "classified_summaries": {
        "Work": ["Project meeting notes", "Client feedback"],
        "Personal": ["Birthday invitation"],
        "Spam": ["Promotion offer"]
    }
}
```


## **6. Helper Functions**

### **`fetch_emails(target_date=None)`**
#### Description
Fetches emails from Gmail using the authenticated user's credentials. Filters emails by a target date.

#### Parameters
- `target_date` (optional): A `datetime.date` object specifying the date for which emails are fetched.

#### Returns
- A list of emails, each containing:
  - `id`: Email ID.
  - `snippet`: Short text snippet from the email body.
  - `from`: Sender's email address.
  - `time`: Timestamp of the email.

#### Errors
- **User Not Authenticated**: Raises `ValueError` if credentials are missing or expired.


## Notes

1. **Authentication**: Ensure that Google OAuth credentials are properly set up before using the API.
2. **MongoDB Setup**: Ensure MongoDB is running locally or update the connection string for remote access.
3. **Environment Variables**:
   - `TEMP`: Path to the Google client secrets file.
   - `OAUTHLIB_INSECURE_TRANSPORT`: Set to `1` for local development only.

4. **Dependencies**:
   - Flask
   - Google APIs client library
   - MongoDB
   - `summarize` and `classify` modules (implementations must be provided).

