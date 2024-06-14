# FlaskBlog

A fully-featured blog application built with Flask, supporting user authentication, CRUD operations for posts, custom error pages, pagination, and more.

## Unique Selling Points (USPs)

- **User Authentication:**
  - **Register:** Create a new account to start blogging.
  - **Login:** Access your account securely with password protection.
  - **Logout:** Securely end your session.

- **User Account Management:**
  - **Update Profile:** Change your username, email, and profile picture.
  - **Password Management:** Securely update your password using Flask-Bcrypt for hashing.

- **Blog Post Management:**
  - **Create Posts:** Write and publish new blog posts with a rich text editor.
  - **Read Posts:** Browse all posts with user-friendly pagination.
  - **Update Posts:** Edit your existing posts.
  - **Delete Posts:** Remove posts you no longer want to display.

- **Interactive Features:**
  - **Pagination:** Easily navigate through multiple pages of posts.
  - **Search:** Quickly find posts by keywords (if implemented).
  - **Commenting:** Allow users to comment on posts (if implemented).

- **Custom Error Pages:**
  - Beautifully designed error pages for 403 (Forbidden), 404 (Not Found), and 500 (Internal Server Error).

- **Email Notifications:**
  - Receive email notifications for account actions (e.g., registration, password reset).

- **Security:**
  - **Password Protection:** Use Flask-Bcrypt to hash passwords.
  - **Session Management:** Secure user sessions with Flask-Login.

- **Modular Code Structure:**
  - Organized with Flask Blueprints for scalability and maintainability.

