# Fetching Places - API Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Get list of places
    API->>BusinessLogic: Fetch available places
    BusinessLogic->>Database: Retrieve places from DB
    Database-->>BusinessLogic: Send data
    BusinessLogic-->>API: Return places list
    API-->>User: Display places
