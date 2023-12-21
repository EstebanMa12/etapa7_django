# The great API for a AvanzatechBlog

## Introduction
This is the official documentation of the Avanzatech Blog API. It provides detailed information about each endpoint, including method description, request and response formats, and examples

## Requeriments
- Python 3.6+
- Django 2.2+
- Django REST Framework 3.10+

## Instalation
First, clone the repository on your local machine:
$ git clone https://github.com/AvanzaTech/blog_api.git

pipenv install
pipenv shell



## API endpoints

### 1. Admin
- Endpoint: admin/
- Description: Allows access to the administration panel to control all models.

### 2. User
- Endpoint: user/login
    - Description: Allows user to login
- Endpoint: user/logout
    - Description: Logs out the user

3. Post
Endpoint: post-create [name='post-create']

Description: Requires user authentication. Allows the creation of a post, automatically saved with the user's name. Displays a list of all accessible posts.
Endpoint: post/<int:id> [name='post']

Description: Provides a detailed view of the post identified by the given ID.
Endpoint: blog/<int:id> [name='post-edit']

Description: Allows editing of the post identified by the provided ID.
Endpoint: post/<int:post_id>/like/ [name='like-create-delete']

Description: Enables liking or unliking a post, provided the user has read permissions. Users can like a post only once.
Endpoint: post/<int:post_id>/comment [name='comment-create-delete']

Description: Facilitates the creation and deletion of comments on the selected post.
Endpoint: post/<int:pk>/delete/ [name='post-delete']

Description: Allows the deletion of a post if the user has the necessary permissions.
4. Likes
Endpoint: likes/
Description: Lists the likes accessible to the user. Users can filter by user_id and post_id.
5. Comments
Endpoint: comments/
Description: Lists the comments accessible to the user. Users can filter by user_id and post_id.
6. Documentation
Endpoint: docs/
Description: Displays API documentation.


Usage
Admin Panel: Access the administration panel via admin/.

User Operations:

Log in: user/login
Log out: user/logout
Post Operations:

Create a post: post-create
View a post: post/<int:id>
Edit a post: blog/<int:id>
Like or unlike a post: post/<int:post_id>/like/
Create or delete comments: post/<int:post_id>/comment
Delete a post: post/<int:pk>/delete/
Likes and Comments:

View likes: likes/
Filter likes by user_id and post_id.
View comments: comments/
Filter comments by user_id and post_id.
Documentation:

Access API documentation: docs/

