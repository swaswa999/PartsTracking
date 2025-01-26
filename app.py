from flaskapp import create_app

# Initialize the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)