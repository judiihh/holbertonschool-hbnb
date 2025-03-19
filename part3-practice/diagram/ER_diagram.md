erDiagram
    USER {
        int id PK
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACE {
        int id PK
        string title
        string description
        float price
        float latitude
        float longitude
        int owner_id
    }

    REVIEW {
        int id PK
        string text
        int rating
        int user_id
        int place_id
    }

    AMENITY {
        int id PK
        string name
    }

    PLACE_AMENITY {
        int place_id PK
        int amenity_id PK
    }

    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE ||--o{ PLACE_AMENITY : includes
    AMENITY ||--o{ PLACE_AMENITY : belongs
