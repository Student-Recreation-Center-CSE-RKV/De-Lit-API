Here's the documentation for the FastAPI endpoints for the blogs page:

### 1. **Upload Blog**: `PUT /blog_upload`
   - **Description**: Upload a new blog to the database.
   - **Request Body**:
     - `author` (string, required): The author of the blog.
     - `blog_name` (string, required): The name of the blog.
     - `link` (string, required): The link to the blog.
     - `content` (string, required): The content of the blog.
     - `overview` (string, required): A brief overview of the blog.
   - **Response**:
     - On success: Returns the blog with the newly created `_id`.
     - On failure: Returns an error message.
   - **Example**:
     - **Request**:
       ```json
       {
         "author": "John Doe",
         "blog_name": "My First Blog",
         "link": "http://example.com/my-first-blog",
         "content": "This is my first blog post.",
         "overview": "A brief overview of my first blog."
       }
       ```
     - **Response** (success):
       ```json
       {
         "_id": "615f77c3f50b7b0a2b9e4f15",
         "author": "John Doe",
         "blog_name": "My First Blog",
         "link": "http://example.com/my-first-blog",
         "content": "This is my first blog post.",
         "overview": "A brief overview of my first blog."
       }
       ```
     - **Response** (error):
       ```json
       {
         "error": "Description of the error"
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
           "author": "John Doe",
           "blog_name": "My First Blog",
           "link": "http://example.com/my-first-blog",
           "content": "This is my first blog post.",
           "overview": "A brief overview of my first blog."
         }
       ]
       ```
     - **Response** (error):
       ```json
       {
         "error": "No blogs found. Please upload blogs before fetching."
       }
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
         "author": "John Doe",
         "blog_name": "My First Blog",
         "link": "http://example.com/my-first-blog",
         "content": "This is my first blog post.",
         "overview": "A brief overview of my first blog."
       }
       ```
     - **Response** (error):
       ```json
       {
         "error": "Invalid ID format"
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
       - `link` (string, optional): New link to the blog.
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
     - **Response** (error):
       ```json
       {
         "error": "No data provided for update"
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
     - **Response** (error):
       ```json
       {
         "error": "Invalid blog ID format"
       }
       ```

---

### Summary of Endpoints:

1. **PUT /blog_upload** - Upload a new blog.
2. **GET /all_blogs** - Retrieve all blogs.
3. **GET /{id}** - Retrieve a specific blog by ID.
4. **PUT /update_blog/{id}** - Update a blog by ID.
5. **DELETE /remove_blog/{blog_id}** - Remove a blog by ID.
