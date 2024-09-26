
# API Documentation for home page get and update endpoints

This document provides a comprehensive overview of the FastAPI application endpoints that manage various content sections in a database. Each section can be retrieved and updated through specific endpoints.

## Base URL

The API can be accessed via the following base URL: 
```
http://localhost:8000/home/
```

## Endpoints Overview

### 1. Retrieve Content Section

- **Endpoint**: `/get_{section}`
- **Method**: `GET`
- **Description**: Fetches the content of the specified section (e.g., contact, magazine, about, blog, clubtalk).
  
#### Request Parameters

- **section**: The name of the section you want to retrieve (e.g., `contact`, `magazine`, etc.).

#### Response Format

- **Success Response**:
  ```json
  {
    "_id": "unique_id",
    "name": "{section_name}",
    "content": "{content_text}",
    "link": "{link_url}"
  }
  ```

- **Error Response**:
  If the section does not exist:
  ```json
  {
    "error": "{section_name} section not found"
  }
  ```

### Example: Get Magazine Section

- **Endpoint**: `/get_magazine`
- **Full URL**: `http://localhost:8000/home/get_magazine`
- **Response**:
  - **Success**:
    ```json
    {
      "_id": "unique_id",
      "name": "magazine",
      "content": "Lorem ipsum",
      "link": "https://raw.githubusercontent.com/venkataPhanindraVutla/Demo-Names/blob/main/sample.jpg"
    }
    ```
  - **Error**:
    ```json
    {
      "error": "magazine section not found"
    }
    ```

### 2. Update Content Section

- **Endpoint**: `/update_{section}`
- **Method**: `PUT`
- **Description**: Updates the content of the specified section. If the section does not exist, it creates a new one.

#### Request Body

- **Content-Type**: `application/json`
- **Schema**:
  ```json
  {
    "name": "{section_name}",
    "content": "{content_text}",
    "link": "{link_url}"
  }
  ```

#### Response Format

- **Success Response**:
  - If updated:
    ```json
    {
      "message": "{section_name} updated successfully"
    }
    ```
  - If created:
    ```json
    {
      "message": "{section_name} created successfully"
    }
    ```

### Example: Update Magazine Section

- **Endpoint**: `/update_magazine`
- **Full URL**: `http://localhost:8000/home/update_magazine`
- **Request Body**:
  ```json
  {
    "name": "magazine",
    "content": "Lorem ipsum",
    "link": "https://raw.githubusercontent.com/venkataPhanindraVutla/Demo-Names/blob/main/sample.jpg"
  }
  ```
- **Response**:
  - **Success**:
    ```json
    {
      "message": "Magazine updated successfully"
    }
    ```
    or
    ```json
    {
      "message": "Magazine created successfully"
    }
    ```

---