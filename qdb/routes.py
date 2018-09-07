from qdb import app

from datetime import datetime
from flask import (
    url_for,
    render_template,
    jsonify,
    redirect,
    abort,
    flash,
    request,
    session,
)
from qdb.models import Quote
from qdb.format import prepare_quote
from qdb.database import db_session
from qdb.utils import Paginator, is_spam
from sqlalchemy.sql.expression import func
import qdb.ircbot as ircbot


@app.route("/")
def home():
    query = db_session.query(Quote).filter(Quote.approved == True)

    order = request.args.get("order", "desc").lower()
    if order == "asc":
        query = query.order_by(Quote.submitted_at.asc()).order_by(Quote.id.asc())
    else:
        query = query.order_by(Quote.submitted_at.desc()).order_by(Quote.id.desc())

    search = request.args.get("s")
    if search:
        query = query.filter(Quote.body.ilike("%" + search + "%"))

    try:
        page = int(request.args.get("p", 1))
    except ValueError:
        resp = jsonify(error="invalid page number")
        resp.status_code = 400
        return resp

    if page < 1:
        page = 1
    paginator = Paginator(query, page, request.url)
    quotes = paginator.items

    if request.headers.get("Accept") == "application/json":
        return jsonify(quotes=paginator)

    return render_template("list.html.jinja", quotes=quotes, paginator=paginator)


@app.route("/all")
def get_all():
    query = db_session.query(Quote).filter(Quote.approved == True)

    order = request.args.get("order", "desc").lower()
    if order == "asc":
        query = query.order_by(Quote.submitted_at.asc()).order_by(Quote.id.asc())
    else:
        query = query.order_by(Quote.submitted_at.desc()).order_by(Quote.id.desc())

    quotes = query.all()

    if request.headers.get("Accept") == "application/json":
        return jsonify(quotes=quotes)

    return render_template("list.html.jinja", quotes=quotes)


@app.route("/random")
def random():
    query = db_session.query(Quote)

    search = request.args.get("s")
    if search:
        query = query.filter(Quote.body.ilike("%" + search + "%"))

    query = query.filter(Quote.approved == True).order_by(func.random()).limit(10)

    quotes = query.all()

    if request.headers.get("Accept") == "application/json":
        return jsonify(quotes=quotes)

    return render_template("list.html.jinja", quotes=quotes)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method in ("GET", "HEAD"):
        return render_template("form.html.jinja", body="")

    if is_spam(request.form["body"]):
        return abort(400)

    body = prepare_quote(
        request.form["body"],
        strip_timestamps=bool(request.form.get("strip_timestamps")),
    )
    if not body:
        return abort(400)
    quote = Quote(body, datetime.now(), request.remote_addr)
    if session.get("logged_in"):
        quote.approved = True
    db_session.add(quote)
    db_session.commit()

    if app.config.get("ENABLE_IRCBOT_WEBHOOKS"):
        ircbot.notify_bot(quote)

    flash("Quote added!")
    return redirect(url_for("home"))


@app.route("/pending")
def pending():
    if not session.get("logged_in"):
        flash("You must be logged in to do that!")
        return redirect(url_for("home"))

    query = (
        db_session.query(Quote)
        .filter(Quote.approved == None)
        .order_by(Quote.submitted_at.desc())
    )

    quotes = query.all()

    if request.headers.get("Accept") == "application/json":
        return jsonify(quotes=quotes)

    return render_template("list.html.jinja", quotes=quotes)


@app.route("/rejected")
def rejected():
    query = db_session.query(Quote).filter(Quote.approved == False)

    order = request.args.get("order", "desc").lower()
    if order == "asc":
        query = query.order_by(Quote.submitted_at.asc()).order_by(Quote.id.asc())
    else:
        query = query.order_by(Quote.submitted_at.desc()).order_by(Quote.id.desc())

    page = int(request.args.get("p", 1))
    if page < 1:
        page = 1
    paginator = Paginator(query, page, request.url)
    quotes = paginator.items

    if request.headers.get("Accept") == "application/json":
        return jsonify(quotes=paginator)

    return render_template("list.html.jinja", quotes=quotes, paginator=paginator)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        flash("You are already logged in!")
        return redirect(url_for("home"))

    if request.method in ("GET", "HEAD"):
        return render_template("login.html.jinja")

    if request.form.get("password") == app.config.get("PASSWORD"):
        session["logged_in"] = True
        flash("Successfully logged in!")
        return redirect(url_for("home"))

    flash("Incorrect password!")
    return redirect(url_for("login"))


@app.route("/<int:quote_id>", methods=["GET", "DELETE", "PATCH"])
def show(quote_id):
    quote = db_session.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        return abort(404)

    if request.method in ("GET", "HEAD"):
        if request.headers.get("Accept") == "application/json":
            return jsonify(quote=quote)
        return render_template("show.html.jinja", quote=quote)

    if not session.get("logged_in"):
        return abort(401)

    if request.method == "DELETE":
        db_session.delete(quote)
        db_session.commit()
        return "OK"

    quote.body = prepare_quote(
        request.form["body"],
        strip_timestamps=bool(request.form.get("strip_timestamps")),
    )
    db_session.add(quote)
    db_session.commit()
    return "OK"


@app.route("/<int:quote_id>/approve", methods=["POST"])
def approve(quote_id):
    if not session.get("logged_in"):
        return abort(401)

    quote = db_session.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        return abort(404)

    quote.approved = True
    db_session.add(quote)
    db_session.commit()

    if app.config.get("ENABLE_IRCBOT_WEBHOOKS"):
        ircbot.notify_bot(quote)

    return "OK"


@app.route("/<int:quote_id>/reject", methods=["POST"])
def reject(quote_id):
    if not session.get("logged_in"):
        return abort(401)

    quote = db_session.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        return abort(404)

    quote.approved = False
    db_session.add(quote)
    db_session.commit()

    return "OK"
