from flask import Blueprint
from flask_login import login_required, current_user
acc = Blueprint("acc", __name__)

@acc.route("/profile")
@login_required
def profile():
  return "login has been done"

@acc.route("/chat", methods=["POST"])
@login_required
def chatroom():
  return "chatroom"