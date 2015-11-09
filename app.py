from flask import Flask, render_template, redirect, jsonify, request, session
from blitzdb import FileBackend, Document

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
backend = FileBackend("./stockr-db")
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Models for storing push subscriber IDs as well as stock data. The Subscriber model will have 
# a subscriber's email address as well as his/her Pushcrew subscriber ID. The Stock model will
# store stock symbols and their last price count, as well as the price bar the subscriber wants
# to use as a measure of when to be notified.

class Subscriber(Document):
	pass

class Stock(Document):
	pass

# Yeah, that's it. 

@app.route('/index', methods=['GET', 'POST'])
def index_view():
	if request.method == 'POST':
		email = request.form['email']
		subscriber_query = backend.get(Subscriber, {'email': email})
		try:
			return redirect('/dashboard')
		except Subscriber.DoesNotExist:
			new_subscriber = Subscriber({'email': email, 'subscriber_id': ''})
			new_subscriber.stocks = []
			backend.save(new_subscriber)
			backend.commit()
			return redirect('/subscribe')
	return render_template('/index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8600)