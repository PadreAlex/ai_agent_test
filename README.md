# AI Agent test task
## DISCLAIMER: THE APP WAS TESTED ON WINDOWS SUBSYSTEM FOR LINUX + NVIDIA GPU.

## How to launch app
### Step one:
Get a key for GeminiAI: [Google dev gemini-api](https://ai.google.dev/gemini-api/docs/api-key) \
Insert your api key in `docker-compose.yml` file
```
GOOGLE_API_KEY=insert_your_api_key
```

### Second step:

Simply run
```
docker compose up -d
```

Now you can call api by following link

```
http://localhost:3000/response_question
```

Don`t forget that this is a POST method \
With raw body:

```
{
    "question": "My Item is damaged"
}
```

### Known issues:

1) I should say that nodejs sometimes does not want to connect to rqm. Simply restart.
2) Flyway sometimes say that it can`t connect to postgres, to migrate sql file. Drop containers and restart.