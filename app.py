from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'auctioneer_name': 'Zach Fonseca',
        'title': 'First Auction',
        'item': '2016 Corvette Z06',
        'date_posted': 'November 15, 2019'
    },

    {
        'auctioneer_name': 'Peter Galvao',
        'title': 'Second Auction',
        'item': 'Pikachu Illustrator Promo Card',
        'date_posted': 'November 16, 2019'
    },

    {
        'auctioneer_name': 'Dominic DeAndrade',
        'title': 'Third Auction',
        'item': 'Collectors Edition Figure',
        'date_posted': 'November 17, 2019'
    },

    {
        'auctioneer_name': 'Carlos Lopes',
        'title': 'Fourth Auction',
        'item': 'Bed Frame',
        'date_posted': 'November 18, 2019'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/info")
def about():
    return render_template('info.html', title='Info')

if __name__ == '__main__':
    app.run(debug=True)
