import sys

sys.path.append('webapp/')

from views import webapp

if __name__ == "__main__":
    # Run the web application
    webapp.run(debug=False)