# 🏠 HBnB Project - Part 1

## **📌 Project Overview**
The **HBnB Evolution** project is a simplified version of an Airbnb-like application. This repository contains the **technical documentation** for **Part 1** of the project, focusing on the **system's architecture, business logic, and API interactions**.

## **📂 Contents**
This repository includes:
- **High-Level Architecture Documentation**
- **Business Logic Layer (Class Diagrams)**
- **API Sequence Diagrams**
- **Comprehensive Technical Documentation**

## **📑 Part 1: Technical Documentation**
### **1️⃣ High-Level Architecture**
- **Description**: The system follows a **three-layered architecture** with a **Facade Pattern** for communication.
- **Diagram:**
```mermaid
classDiagram
  class PresentationLayer {
    <<Interface>>
    +ServiceAPI()
  }
  class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
  }
  class PersistenceLayer {
    +DatabaseAccess
  }

  PresentationLayer --> BusinessLogicLayer : Facade Pattern
  BusinessLogicLayer --> PersistenceLayer : Database Operations
```
- **Layers:**
  - **Presentation Layer**: API and User Interface.
  - **Business Logic Layer**: Handles core logic and models.
  - **Persistence Layer**: Manages database storage and retrieval.

### **2️⃣ Business Logic Layer**
- **Entities:** User, Place, Review, and Amenity.
- **Diagram:**
```mermaid
classDiagram
  class User {
    +UUID id
    +String first_name
    +String last_name
    +String email
    +String password
    +Boolean is_admin
    +Date created_at
    +Date updated_at
    +register()
    +update_profile()
    +delete()
  }

  class Place {
    +UUID id
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +Date created_at
    +Date updated_at
    +create_place()
    +update_place()
    +delete_place()
  }

  class Review {
    +UUID id
    +UUID user_id
    +UUID place_id
    +Integer rating
    +String comment
    +Date created_at
    +Date updated_at
    +create_review()
    +update_review()
    +delete_review()
  }

  class Amenity {
    +UUID id
    +String name
    +String description
    +Date created_at
    +Date updated_at
    +create_amenity()
    +update_amenity()
    +delete_amenity()
  }

  User --> Place : owns
  User --> Review : writes
  Place --> Review : has
  Place --> Amenity : contains
```
- **Relationships:**
  - Users can own multiple places.
  - Users can write multiple reviews.
  - Places contain multiple amenities.

### **3️⃣ API Interaction Flow**
The **API handles key operations** for users, places, reviews, and amenities.

#### **📌 API Sequence Diagrams**
| API Call | Description |
|----------|------------|
| **User Registration** | Registers a new user in the system |
| **Place Creation** | Allows a user to create a new listing |
| **Review Submission** | Users can submit reviews for places |
| **Fetching Places** | Retrieves a list of available places |

#### **User Registration**
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
```

#### **Place Creation**
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
```

#### **Review Submission**
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
```

#### **Fetching Places**
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
```

## **🚀 How to Use This Repository**
### **Clone the Repository**
```sh
 git clone https://github.com/judiihh/holbertonschool-hbnb.git
```

### **View the Documentation**
1. Open the `README.md` to understand the project structure.
2. Navigate to `docs/` to find detailed technical diagrams.

## **💡 Future Work**
This is only **Part 1** of the project. Future phases will include:
- Database integration
- Backend API development
- Frontend implementation

## **👤 Author**
- **Judith Espinal** - Holberton School Student
