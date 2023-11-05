from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)

with open('storage.json', 'r') as json_file:
    blog_posts = json.load(json_file)


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


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
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    # Remove the blog post with the specified post_id
    blog_posts.remove(post)

    # Save the updated blog posts to the JSON file
    with open('storage.json', 'w') as json_file:
        json.dump(blog_posts, json_file, indent=2)

    # Redirect to the index
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    '''
    Displays a form for updating the blog post with the given post_id.
    :param post_id: The ID of the blog post to be updated.
    :return: Rendered template for updating the blog post.
    '''
    # Fetch the blog post from the JSON file using the fetch_post_by_id function
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Save the updated blog posts to the JSON file
        with open('storage.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=2)

        # Redirect back to the index page
        return redirect(url_for('index'))

    # If it's a GET request, display the update.html page with the current post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
