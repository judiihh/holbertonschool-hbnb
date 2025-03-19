```mermaid
erDiagram
    USERS {
      int id PK
      string username
      string first_name
      string last_name
      string email
      string password_hash
      boolean is_admin
      datetime created_at
      datetime updated_at
    }

    PLACES {
      int id PK
      string name
      string description
      int price
      int owner_id FK
      datetime created_at
      datetime updated_at
    }

    REVIEWS {
      int id PK
      string content
      int rating
      int user_id FK
      int place_id FK
      datetime created_at
      datetime updated_at
    }

    AMENITIES {
      int id PK
      string name
      string description
      datetime created_at
      datetime updated_at
    }

    PLACE_AMENITY {
      int place_id PK FK
      int amenity_id PK FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : has
    PLACES ||--o{ PLACE_AMENITY : linked
    AMENITIES ||--o{ PLACE_AMENITY : linked
```
