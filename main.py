from replit import db
from flask import Flask, render_template, request, session
import secrets

secret = secrets.token_urlsafe(32)

app = Flask(__name__)
app.secret_key = secret
app.config['SESSION_TYPE'] = 'filesystem'


# Checks if all of the supplied values for the database are initialised and if not creates them with 0 votes.
for poll_option in open("current_poll.txt", "r").readlines()[1].split("#"):
  try:
    foo = db[poll_option]
  except:
    db[poll_option] = 0

# LEGACY - Checks if the database is set up and displays key missing
for poll_option in open("current_poll.txt", "r").readlines()[1].split("#"):
  try:
    foo = db[poll_option]
  except:
    print(f"Database is not set up correctly, please allocate a value for {poll_option}")
    
# Outputs database content into console, can be disabled if not needed
for key in db.keys():
  print(f"{key[0].upper()}{key[1:]} has: {str(db[key])} votes.")

# Directs the user to the home page from root.
@app.route('/')
def home():
  x = session.get('submitting', None)
  if not x:
    session['submitting'] = 1
  poll_name = " ".join((open("current_poll.txt").readlines()[0]).split(" "))
  options = (open("current_poll.txt").readlines()[1]).split("#")
  return render_template("home.html", poll_name = poll_name, options = options)

# Re-directs user to home page from other pages
@app.route('/home.html')
def return_home():
  session["submitting"] = 1
  poll_name = " ".join((open("current_poll.txt").readlines()[0]).split(" "))
  options = (open("current_poll.txt").readlines()[1]).split("#")
  return render_template("home.html", poll_name = poll_name, options = options)

# Directs user to submitted page after they have submitted feedback or a vote on the poll.
@app.route('/submitted.html', methods=["POST"])
def submitted():
  if session.get('submitting', None) == 1:
    option_selected = request.form['options']
    try:
      db[option_selected] += 1
    except:
      pass
  else:
    with open("user_responses/response.txt", "a") as f:
      f.write("\n" + request.form["feedback"])
  return render_template("submitted.html")

# Directs user to the results page.
@app.route('/results.html')
def results():
  options = (open("current_poll.txt").readlines()[1]).split("#")
  
  results = []
  for option in options:
    results.append("")
  
  for key in db.keys():
    results[options.index(key)] = db[key]
  words = []
  for option in options:
    word1 = str(option)[0].upper() + str(option)[1:]
    word2 = str(results[options.index(option)])[0].upper() + str(results[options.index(option)])[1:]
    word_pair = []
    word_pair.append(word1)
    word_pair.append(word2)
    words.append(word_pair)
  total_votes = 0
  for pair in words:
    total_votes += int(pair[1])
  print(total_votes)
    
  return render_template("results.html", words = words, total_votes = total_votes)

# Directs user to the feedback page.
@app.route('/feedback.html', methods=["GET", "POST"])
def feedback():
  session["submitting"] = 0
  return render_template("feedback.html")

# Runs the app if the file is main.
if __name__ == '__main__':
  app.run(host='0.0.0.0')