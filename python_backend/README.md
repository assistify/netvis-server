# Python program for loading and filtering data from RC database

## Requirements
- Docker
- MongoDB with RC database
- Netvis server

## Configuration
The container can be configured with the following environment variables:

| Name | Description | Example |
| ---- | ----------- | ------- |
| DATA_COUNT | Number of Messages processed | 500000 | 
| FILTERW | Threshold for word occurance | 10 |
| MONGO_DB | Name of RC Database | Team |
| MONGO_URL | URL of the MongoDB | mongodb://host.docker.internal:27017 |
| SERVER_URL | Netvis server URL | http://host.docker.internal:3002 |
| SKIP_TYPES | Room types to skip | "cdp" |

Create an `.env` file with the desired variables.

## Build & Run
`docker build -t rcanalysis .`
`docker run --env-file=.env rcanalysis`


## Filter Components

### Database filter
- Every symbols but letters are removed
- Every message is split into their words
- Every word with less then 3 characters are removed

### Word type filter
- Words are filter for nouns and names

### Occurance filter
- Every word which occures less then x times is removed, where x is defined via environment variables

### Optional room type filter
- Messages belonging to specific room types can be skipped, configured by environment variable SKIP_TYPES

## Output format
The output is stored in the following json format:
```
[
    {
        "name": "Name of the room",
        "type": "Type of the room"
        "topics": [
            {
                "name": "word",
                "weight": "occurance inside the room",
                "maxWeight": "occurance over all rooms"
            }
        ],
        "users": [
            "Name of the member of the room"
        ]
    }
]
```
