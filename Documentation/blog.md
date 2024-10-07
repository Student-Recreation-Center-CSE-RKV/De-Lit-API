# Blog API Documentation

## Introduction
This API allows users to upload, retrieve, update, and delete blog entries in the **Delit-test** MongoDB database. Each blog entry consists of the author's name, blog title, link, content, an overview, and a timestamp for when the blog was created.

The API uses **FastAPI** for handling HTTP requests and **Pydantic** for data validation. MongoDB's `ObjectId` is used to uniquely identify each blog entry.

## API Endpoints

### 1. Upload Blog Entry
- **Method**: `POST`
- **Endpoint**: `/blog`
- **Description**: Upload a new blog entry to the database.
- **Request Body**: 
  ```json
  {
    "author": "string",
    "blog_name": "string",
    "link": "string",
    "content": "string",
    "overview": "string"
  }
  ```
  > The `created_at` field is automatically generated upon blog creation.
- **Response**:
  ```json
  {
    "_id": "67037455bd41e77da7f836b7",
    "author": "De-lit Admin",
    "blog_name": "Broken piece of heart",
    "link": "https://test.link",
    "content": "test data",
    "overview": "overview",
    "created_at": "2024-10-07T11:10:37.674000"
  }
  ```
- **Error Codes**:
  - `400`: Blog could not be uploaded to the database.
  - `500`: An unknown error occurred.

### 2. Retrieve All Blogs
- **Method**: `GET`
- **Endpoint**: `/blog`
- **Description**: Fetch all blog entries from the database, sorted by creation date (latest first).
- **Response**:
  ```json
  [
    {
      "_id": "67037455bd41e77da7f836b7",
      "author": "De-lit Admin",
      "blog_name": "Broken piece of heart",
      "link": "https://test.link",
      "content": "test data",
      "overview": "overview",
      "created_at": "2024-10-07T11:10:37.674000"
    }
  ]
  ```
- **Error Codes**:
  - `404`: No blogs found in the database.
  - `500`: An unknown error occurred.

### 3. Retrieve a Single Blog by ID
- **Method**: `GET`
- **Endpoint**: `/blog/{id}`
- **Description**: Retrieve a specific blog entry by its unique MongoDB `ObjectId`.
- **Request Parameters**:
  - `id`: The `ObjectId` of the blog you want to retrieve.
- **Response**:
  ```json
  {
    "_id": "67037455bd41e77da7f836b7",
    "author": "De-lit Admin",
    "blog_name": "Broken piece of heart",
    "link": "https://test.link",
    "content": "test data",
    "overview": "overview",
    "created_at": "2024-10-07T11:10:37.674000"
  }
  ```
- **Error Codes**:
  - `404`: Invalid blog ID format or blog not found.
  - `500`: An unknown error occurred.

### 4. Update Blog by ID
- **Method**: `PUT`
- **Endpoint**: `/blog/{id}`
- **Description**: Update a specific blog entry by its `ObjectId`. Only the provided fields will be updated; other fields will remain unchanged.
- **Request Parameters**:
  - `id`: The `ObjectId` of the blog to update.
- **Request Body** (Optional fields):
  ```json
  {
    "author": "string",
    "blog_name": "string",
    "link": "string",
    "content": "string",
    "overview": "string"
  }
  ```
- **Response**:
  - `200`: Blog updated successfully.
- **Error Codes**:
  - `400`: No data provided for update.
  - `404`: Invalid blog ID format or blog not found.
  - `500`: An unknown error occurred.

### 5. Delete Blog by ID
- **Method**: `DELETE`
- **Endpoint**: `/blog/{blog_id}`
- **Description**: Delete a specific blog by its `ObjectId`.
- **Request Parameters**:
  - `blog_id`: The `ObjectId` of the blog to delete.
- **Response**:
  - `200`: Blog successfully deleted.
- **Error Codes**:
  - `404`: Invalid blog ID format or blog not found.
  - `500`: Failed to delete the blog or an unknown error occurred.

## Usage Example

1. **POST Request Example**:
   ```json
   {
     "author": "De-lit Admin",
     "blog_name": "Broken piece of heart",
     "link": "https://test.link",
     "content": "test data",
     "overview": "overview"
   }
   ```
   Response:
   ```json
   {
     "_id": "67037455bd41e77da7f836b7",
     "author": "De-lit Admin",
     "blog_name": "Broken piece of heart",
     "link": "https://test.link",
     "content": "test data",
     "overview": "overview",
     "created_at": "2024-10-07T11:10:37.674000"
   }
   ```

## Access
This blog is available at the following endpoint:

**Base URL**: `localhost:8000`
- **Endpoint**: `/blog` 

## Error Handling

All endpoints are wrapped with an exception handler to manage known and unknown errors. If an unexpected error occurs, the system will return a 500 status code with a descriptive error message.

### Summary of Endpoints:

1. **PUT /** - Upload a new blog.
2. **GET /** - Retrieve all blogs.
3. **GET /{blog_id}** - Retrieve a specific blog by ID.
4. **PUT /{blog_id}** - Update a blog by ID.
5. **DELETE /{blog_id}** - Remove a blog by ID.

> **Note**: The `link` field in each blog entry refers to the **contact link for the author**.