from flask import render_template, url_for, flash, redirect, request, abort
from flaskauction import app, db, bcrypt
from flaskauction.forms import RegistrationForm, LoginForm, AuctionForm
from flaskauction.models import User, Auction
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    auctions = Auction.query.all()
    return render_template('home.html', auctions=auctions)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        flash(f'Account has successfully been created for {form.username.data}.', 'success')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully created an account!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Attempt Failed. Please check Username and Password.' , 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/auction/new", methods=['GET', 'POST'])
@login_required
def new_auction():
    form = AuctionForm()
    if form.validate_on_submit():
        auction = Auction(auction_name=form.auction_name.data, item=form.item.data, item_description=form.item_description.data, asking_price=form.asking_price.data, auctioneer=current_user)
        db.session.add(auction)
        db.session.commit()
        flash('Your auction has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('create_auction.html', title='New Auction', form= form, legend='New Auction')


@app.route("/auction/<int:auction_id>")
def auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    return render_template('auction.html', title=auction.auction_name, auction=auction)


@app.route("/auction/<int:auction_id>/update", methods=['GET', 'POST'])
@login_required
def update_auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    if auction.auctioneer != current_user:
        abort(403)
    form = AuctionForm()
    if form.validate_on_submit():
        auction.auction_name = form.auction_name.data
        auction.item = form.item.data
        auction.item_description = form.item_description.data
        auction.asking_price = form.asking_price.data
        db.session.commit()
        flash('Your auction was successfully updated.', 'success')
        return redirect(url_for('auction', auction_id=auction.id))
    elif request.method == 'GET':
        form.auction_name.data = auction.auction_name
        form.item.data = auction.item
        form.item_description.data = auction.item_description
        form.asking_price.data = auction.asking_price
    return render_template('create_auction.html', title='Update Auction', form=form, legend='Update Auction')


@app.route("/auction/<int:auction_id>/delete", methods=['POST'])
@login_required
def delete_auction(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    if auction.auctioneer != current_user:
        abort(403)
    db.session.delete(auction)
    db.session.commit()
    flash('Your auction was successfully deleted.', 'success')
    return redirect(url_for('home'))
