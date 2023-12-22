# The great API for a AvanzatechBlog

## Introduction
This is the official documentation of the Avanzatech Blog API. It provides detailed information about each - Endpoint, including method description, request and response formats.

## Requeriments
- Python 3.6+
- Django 2.2+
- Django REST Framework 3.10+

## Instalation
First, clone the repository on your local machine:
~~~
$ git clone git@github.com:EstebanMa12/etapa7_django.git

pipenv install #To install all dependencies
pipenv shell   # To enter in virtual environment
python manage.py migrate # To create database tables
python manage.py createsuperuser #To create a super user

python manage.py runserver # To deploy  
~~~



## API Endpoints

### 1. Admin
- Endpoint: <code>admin/</code>
    - Description: Allows access to the administration panel to control all models.

### 2. User
- Endpoint: <code>user/login</code>
    - Description: Allows user to login
- Endpoint: <code>user/logout</code>
    - Description: Logs out the user

### 3. Post
- Endpoint: <code>post/</code> [name='post-create']

    - Description: Requires user authentication. Allows the creation of a post, automatically saved with the user's name. Displays a list of all accessible posts.
- Endpoint: <code>post/<int:id></code> [name='post']

    - Description: Provides a detailed view of the post identified by the given ID.
- Endpoint:<code> blog/<int:id></code> [name='post-edit']

    - Description: Allows editing of the post identified by the provided ID.
- Endpoint: <code>post/<int:post_id>/like/</code> [name='like-create-delete']

    - Description: Enables liking or unliking a post, provided the user has read permissions. Users can like a post only once.
- Endpoint: <code>post/<int:post_id>/comment</code> [name='comment-create-delete']

    - Description: Facilitates the creation and deletion of comments on the selected post.
- Endpoint: <code>post/<int:pk>/delete/</code> [name='post-delete']

    - Description: Allows the deletion of a post if the user has the necessary permissions.
### 4. Likes
- Endpoint: <code>likes/</code>
    - Description: Lists the likes accessible to the user. Users can filter by user_id and post_id.
### 5. Comments
- Endpoint: <code>comments/</code>
    - Description: Lists the comments accessible to the user. Users can filter by user_id and post_id.
### 6. Documentation
- Endpoint: <code>docs/</code>
    - Description: Displays API documentation.


## Usage
Admin Panel: Access the administration panel via <code> admin/.</code>

### User Operations:

    Log in: user/login
    Log out: user/logout

### Post Operations:

    Create a post:post/

    View a post: post/<int:id>

    Edit a post: blog/<int:id>

    Like or unlike a post: post/<int:post_id>/like/

    Create or delete comments: post/<int:post_id>/comment

    Delete a post: post/<int:pk>/delete/


### Likes and Comments:

    View likes: likes/

    Filter likes: likes/?user_id=X&post_id=Y

    View comments: comments/

    Filter comments: comments/?user_id=X&post_id=Y

### Documentation:

    Access API documentation: docs/

### Tests
To run tests, use the following command:

    pytest



