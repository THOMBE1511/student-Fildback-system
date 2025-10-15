  from flask import Flask, request, redirect, url_for, render_template
  import mysql.connector
  from mysql.connector import Error

  app = Flask(__name__)

  # Database connection function
  def get_db_connection():
      try:
          connection = mysql.connector.connect(
              host='localhost',
              user='root',  # Default XAMPP username
              password='',  # Default XAMPP password (empty)
              database='student_feedback_db'
          )
          return connection
      except Error as e:
          print(f"Error connecting to MySQL: {e}")
          return None

  # Route for the home page (serving the form)
  @app.route('/')
  def index():
      return render_template('index.html')  # Assuming you have index.html in a templates folder

  # Route to handle form submission
  @app.route('/submit-feedback', methods=['POST'])
  def submit_feedback():
      rating = request.form.get('rating')
      feedback_text = request.form.get('feedbackText')
      category = request.form.get('category')
      
      connection = get_db_connection()
      if connection is not None:
          try:
              cursor = connection.cursor()
              query = """INSERT INTO feedback (rating, feedback_text, category) 
                         VALUES (%s, %s, %s)"""
              values = (rating, feedback_text, category)
              cursor.execute(query, values)
              connection.commit()
              cursor.close()
              connection.close()
              return redirect(url_for('thank_you'))  # Redirect to thank you page
          except Error as e:
              return f"Error: {e}"
      else:
          return "Database connection failed"

  # Route for the thank you page
  @app.route('/thank-you')
  def thank_you():
      return "<h1>Thank you for your feedback!</h1><a href='/'>Go back</a>"

  if __name__ == '__main__':
      app.run(debug=True)
  