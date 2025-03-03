# Review Submission - API Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Submit a review
    API->>BusinessLogic: Validate review details
    BusinessLogic->>Database: Store review
    Database-->>BusinessLogic: Confirm success
    BusinessLogic-->>API: Return review ID
    API-->>User: Review successfully added
