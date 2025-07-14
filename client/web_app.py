from client import create_app

# Create the application instance using the factory function
app = create_app()

if __name__ == '__main__':
    # The debug flag will be set based on the environment in a production app,
    # but this is fine for local development.
    app.run(debug=True, host='0.0.0.0', port=5000)
