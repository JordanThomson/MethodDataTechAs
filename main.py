from website import create_app

app = create_app()

# this means that this command will only execute if the file is run directly
if __name__ == '__main__':
    app.run(debug=True) # run flask application, debug means constantly changing the server (easy for production)