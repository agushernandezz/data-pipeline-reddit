# Data pipeline - Reddit
A Reddit data pipeline project for extracting data from any subreddit on Reddit.

The data is automatically ingested, stored, and transformed for later analysis.
 
<img src="https://github.com/agushernandezz/data-pipeline-reddit/blob/main/images/architecture_pipeline.png">
 
## Data Description
 
## Setup
To gather data from Reddit, it's necessary to employ its Application Programming Interface (API) and complete a few setup steps.

1. Create a Reddit account.
2. Navigate here and create an app. Make sure you select "script" from the radio buttons during the setup process.
3. Take a note of a few things once this is setup:
- The App ID (CLIENT_ID)
- API Secret Key (SECRET_KEY)
- Reddit acccount Username (USERNAME)
- Reddit acccount password (PASSWORD)
- The subreddit to extract data (subreddit)
4. Fill the setup.json with the credentials. An example:
```json
{
  "conf": {
    "CLIENT_ID": "asd123client_id",
    "SECRET_KEY": "asd123secret_key",
    "USERNAME": "redditusername",
    "PASSWORD": "redditpassword",
    "subreddit": "funny"
  }
}
```

