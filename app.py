import uuid
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

with open('storage.json', 'r') as json_file:
    blog_posts = json.load(json_file)


@app.route('/')
def index():
    '''
    This route will display all blog posts.
    :return: rendered template: index.html
    '''
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST']) #this route should respond to both GET and POST requests
def add():
    '''
    Displays a form for creating a new blog post if a GET (default method) request is sent,
    and adds a new blog post to storage list if a POST request is sent.
    :return: rendered template: add.html
    '''
    if request.method == 'POST':
        new_post = {
            'id': str(uuid.uuid4()),
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }

        # Add the new blog post to the list
        blog_posts.append(new_post)

        # Save the updated blog posts to the JSON file
        with open('storage.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=2)

        # Redirect to the homepage
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    '''
    Deletes a blog post with the given post_id.
    :param post_id: The ID of the blog post to be deleted.
    :return: Redirect to the homepage after deleting.
    '''
    # Find and remove the blog post with the specified post_id
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    # Save the updated blog posts to the JSON file
    with open('storage.json', 'w') as json_file:
        json.dump(blog_posts, json_file, indent=2)

    # Redirect to the homepage
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run()


#------------------------------------------------------------------------------
