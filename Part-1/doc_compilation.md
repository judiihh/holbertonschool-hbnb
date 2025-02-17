# HBnB Evolution - Technical Documentation

## **1. Introduction**
The **HBnB Evolution** project is a simplified version of an Airbnb-like application. This document serves as a **blueprint** for the system's architecture, business logic, and API interactions. It provides technical insights for implementation, ensuring a **clear structure and functionality** for the project.

The document includes:
- **High-Level Architecture**: Overview of the system layers.
- **Business Logic Layer**: Core models and their relationships.
- **API Interaction Flow**: Sequence diagrams illustrating API interactions.

---

## **2. High-Level Architecture**
### **📌 High-Level Package Diagram**
This diagram illustrates the **three-layer architecture** of the application and how the layers communicate using the **Facade Pattern**.

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

### **🔹 Explanation:**
- **Presentation Layer**: Handles user interactions (e.g., API endpoints).
- **Business Logic Layer**: Contains the core logic (e.g., User, Place, Review, Amenity models).
- **Persistence Layer**: Manages database storage and retrieval.

---

## **3. Business Logic Layer**
### **📌 Class Diagram**
This diagram represents the main entities in the system, their attributes, and relationships.

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

### **🔹 Explanation:**
- **User** owns **multiple Places** and writes **multiple Reviews**.
- **Place** is owned by a **User** and has **multiple Reviews and Amenities**.
- **Review** is linked to both a **User** (who wrote it) and a **Place**.
- **Amenity** is associated with **one or more Places**.

---

## **4. API Interaction Flow**
### **📌 API Sequence Diagrams**
The following sequence diagrams illustrate how different components interact when handling API requests.

#### **1️⃣ User Registration**
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

#### **2️⃣ Place Creation**
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

#### **3️⃣ Review Submission**
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

#### **4️⃣ Fetching a List of Places**
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

---

## **5. Conclusion**
Working on this technical documentation for **HBnB Evolution** has been a challenging but rewarding experience. Organizing the system's **architecture, business logic, and API interactions** into clear diagrams helped me gain a deeper understanding of how all the components fit together. 

One of the most interesting aspects was defining the **relationships between entities**—it made me realize how crucial **data structure planning** is for scalability and efficiency. 

Additionally, designing the **sequence diagrams** allowed me to visualize the exact flow of information between different system layers, reinforcing the importance of **well-structured API interactions**.

Overall, this documentation serves as a **blueprint for implementation**, but also as a personal milestone in my journey toward becoming a more structured and detail-oriented developer. I look forward to applying these principles as the project evolves!
