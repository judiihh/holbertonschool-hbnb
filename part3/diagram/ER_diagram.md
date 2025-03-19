erDiagram
    USERS {
      int id PK "Primary key"
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
      text description
      int price
      int owner_id FK "References USERS(id)"
      datetime created_at
      datetime updated_at
    }

    REVIEWS {
      int id PK
      text content
      int rating
      int user_id FK "References USERS(id)"
      int place_id FK "References PLACES(id)"
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
      int place_id PK FK "References PLACES(id)"
      int amenity_id PK FK "References AMENITIES(id)"
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--o{ PLACE_AMENITY : "linked via"
    AMENITIES ||--o{ PLACE_AMENITY : "linked via"
