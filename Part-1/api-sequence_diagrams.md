# API Sequence Diagrams

## **1️⃣ User Registration**
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


## **2️⃣ Place Creation**
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Create a new place
    API->>BusinessLogic: Validate place data
    BusinessLogic->>Database: Save place details
    Database-->>BusinessLogic: Confirm success
    BusinessLogic-->>API: Return place ID
    API-->>User: Place successfully created


## **3️⃣ Review Submission**
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


## **4️⃣ Fetching a List of Places**
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
