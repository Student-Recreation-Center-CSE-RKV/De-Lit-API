# FastAPI Blog API Documentation

This document provides an overview of the FastAPI application endpoints for managing blogs. The API allows users to upload, retrieve, update, and delete blog entries. 

> **Note:** The `link` field in each blog entry represents the **contact link for the author**.

## Base URL

The API can be accessed via the following base URL:
```
http://localhost:8000/blog/
```

---

## Endpoints Overview

### 1. **Upload Blog**: `PUT /blog_upload`
- **Description**: Upload a new blog to the database.
- **Request Body**:
  - `author` (string, required): The author of the blog.
  - `blog_name` (string, required): The name of the blog.
  - `link` (string, required): The contact link for the author.
  - `content` (string, required): The content of the blog.
  - `overview` (string, required): A brief overview of the blog.
- **Response**:
  - On success: Returns the blog with the newly created `_id`.
  - On failure: Returns an error message.
- **Example**:
  - **Request**:
    ```json
    {
      "author": "Phani",
      "blog_name": "How to Master CP",
      "link": "test_link",
      "content": "Lorem",
      "overview": "Lorem"
    }
    ```
  - **Response** (success):
    ```json
    {
      "_id": "615f77c3f50b7b0a2b9e4f15",
      "author": "Phani",
      "blog_name": "How to Master CP",
      "link": "test_link",
      "content": "Lorem",
      "overview": "Lorem"
    }
    ```

---

### 2. **Get All Blogs**: `GET /all_blogs`
- **Description**: Retrieve all blogs from the database.
- **Response**:
  - On success: Returns a list of all blogs with their respective fields.
  - On failure or no blogs: Returns an error message.
- **Example**:
  - **Response** (success):
    ```json
    [
      {
        "_id": "615f77c3f50b7b0a2b9e4f15",
        "author": "Phani",
        "blog_name": "How to Master CP",
        "link": "test_link",
        "content": "Lorem",
        "overview": "Lorem"
      }
    ]
    ```

---

### 3. **Get Blog by ID**: `GET /{id}`
- **Description**: Retrieve a specific blog by its ID.
- **Path Parameter**:
  - `id` (string, required): The unique MongoDB ObjectID of the blog.
- **Response**:
  - On success: Returns the blog with the specified ID.
  - On failure: Returns an error message (invalid ID, blog not found).
- **Example**:
  - **Request**: `GET /615f77c3f50b7b0a2b9e4f15`
  - **Response** (success):
    ```json
    {
      "_id": "615f77c3f50b7b0a2b9e4f15",
      "author": "Phani",
      "blog_name": "How to Master CP",
      "link": "test_link",
      "content": "Lorem",
      "overview": "Lorem"
    }
    ```

---

### 4. **Update Blog**: `PUT /update_blog/{id}`
- **Description**: Update a blog's details by its ID.
- **Path Parameter**:
  - `id` (string, required): The unique MongoDB ObjectID of the blog to be updated.
- **Request Body**:
  - The fields that can be updated are optional:
    - `author` (string, optional): New author of the blog.
    - `blog_name` (string, optional): New blog name.
    - `link` (string, optional): New contact link for the author.
    - `content` (string, optional): New content of the blog.
    - `overview` (string, optional): New overview of the blog.
- **Response**:
  - On success: Returns a success message indicating the blog was updated.
  - On failure: Returns an error message (invalid ID, no blog found, no data to update).
- **Example**:
  - **Request**:
    ```json
    {
      "author": "Jane Doe",
      "blog_name": "Updated Blog Name"
    }
    ```
  - **Response** (success):
    ```json
    {
      "success": "Blog updated successfully"
    }
    ```

---

### 5. **Delete Blog**: `DELETE /remove_blog/{blog_id}`
- **Description**: Remove a specific blog by its ID.
- **Path Parameter**:
  - `blog_id` (string, required): The unique MongoDB ObjectID of the blog to be deleted.
- **Response**:
  - On success: Returns a success message indicating the blog was deleted.
  - On failure: Returns an error message (invalid ID, blog not found, deletion failed).
- **Example**:
  - **Request**: `DELETE /remove_blog/615f77c3f50b7b0a2b9e4f15`
  - **Response** (success):
    ```json
    {
      "Success": "Blog with id 615f77c3f50b7b0a2b9e4f15 is successfully deleted"
    }
    ```

---

### Summary of Endpoints:

1. **PUT /blog_upload** - Upload a new blog.
2. **GET /all_blogs** - Retrieve all blogs.
3. **GET /{id}** - Retrieve a specific blog by ID.
4. **PUT /update_blog/{id}** - Update a blog by ID.
5. **DELETE /remove_blog/{blog_id}** - Remove a blog by ID.

---

> **Note**: The `link` field in each blog entry refers to the **contact link for the author**.