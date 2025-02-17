# Business Logic Class Diagram

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
