
def home_view(request):
    # cursor = request.db_connection.cursor()
    # try:
        # cursor.execute("SELECT * FROM posts")
        # posts = cursor.fetchall()
        posts = {"a":"a"}
        content = request.render_template('home.html', posts=posts)
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write(content.encode('utf-8'))
    # except sqlite3.Error as e:
        # request.send_error(500, f"Internal Server Error: {str(e)}")


def about_view(request):
    try:
        content = request.render_template('about.html')
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write(content.encode('utf-8'))
    except IOError:
        request.send_error(500, "Internal Server Error")


def contact_view(request):
    try:
        content = request.render_template('contact.html')
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write(content.encode('utf-8'))
    except IOError:
        request.send_error(500, "Internal Server Error")


def submit_view(request, params):
    # try:
        name = params.get('name', [''])[0]
        email = params.get('email', [''])[0]

        # cursor = request.db_connection.cursor()
        # cursor.execute("INSERT INTO submissions (name, email) VALUES (?, ?)", (name, email))
        # request.db_connection.commit()

        content = request.render_template('submit.html', name=name, email=email)
        request.send_response(200)
        request.send_header('Content-type', 'text/html')
        request.end_headers()
        request.wfile.write(content.encode('utf-8'))
    # except sqlite3.Error as e:
        # request.send_error(500, f"Internal Server Error: {str(e)}")

