# User Registration - API Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register new account
    API->>BusinessLogic: Validate user details
    BusinessLogic->>Database: Store user data
    Database-->>BusinessLogic: Confirm success
    BusinessLogic-->>API: Return success message
    API-->>User: Registration successful
