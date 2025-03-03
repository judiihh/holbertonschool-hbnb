# High-Level Package Diagram

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
