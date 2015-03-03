from server import app

from server import api, db, auth
from model import User, Post
from forms import UserCreateForm

from datetime import datetime

from flask import render_template, Blueprint
from flask.ext.restful import Api, Resource, reqparse

from authToken import AuthToken

blueprint = Blueprint('view', __name__, template_folder='templates')

auth = AuthToken()

@app.route("/", methods=("GET","POST"))
def index():

    form = UserCreateForm()

    if form.validate_on_submit():

        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()

    return render_template('index.html', form=form)

@auth.verify_token
def verify_passwd(auth_token):
    user = User.verify_auth_token(auth_token)
    if user:
        return True
    else:
        return False


class postParams:

    """docstring for articleParams"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title', type=str, required=True, help="No title", location='json')
        self.reqparse.add_argument(
            'body', type=str, required=True, help="No content", location='json')

class userParams:

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, help="NO username")
        self.reqparse.add_argument('password', type=str, help="NO password")
        self.reqparse.add_argument('token', type=str, help='NO token')


class postAPI(Resource, postParams):

    """docstring for articleApi"""

    def get(self, id):
        try:
            result = Post.query.filter(Post.id == id).first()
            pst = dict()
            pst.update(result.as_dict())
            pst.update(
                {'author': result.user.email})
            return pst
            # return request.headers.get('Auth',"");
        except Exception as e:
            return False

    @auth.login_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument(
            'title', type=str, required=True, help="No title", location='json')
        parser.add_argument(
            'body', type=str, required=True, help="No content", location='json')

        args = parser.parse_args()

        try:
            post = Post.query.get(id)
            post.title = args['title']
            post.content = args['body']
            db.session.commit()
            return True
        except Exception as e:
            return e.message

    @auth.login_required
    def delete(self, id):
        a = Post.query.get(id)
        db.session.delete(a)
        try:
            db.session.commit()
            return True
        except Exception as e:
            return False


class articlesPageAPI(Resource, postParams):

    """docstring for articleListAPI"""

    def get(self, page, per_page):
        offset = (page - 1) * per_page
        try:
            posts = Post.query.offset(offset).limit(per_page)
            pstList = []
            for post in posts:
                temp = post.as_dict()
                temp.update({"author": post.user.email})
                pstList.append(temp)
            return pstList
        except Exception as e:
            return e.message

class postsAPI(Resource, postParams):

    @auth.login_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            'title', type=str, required=True, help="No title", location='json')
        parser.add_argument(
            'body', type=str, required=True, help="No content", location='json')

        args = parser.parse_args()
        now = datetime.now()
        a = Post(
            user_id=1, title=args['title'], body=args['body'], time=now)
        try:
            db.session.add(a)
            db.session.commit()
            return True
        except Exception as e:
            return False

class userAPI(Resource, userParams):

    """docstring for userAPI"""

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str)
        args = parser.parse_args()

        #args = self.reqparse.parse_args()
        return User.verify_auth_token(args["token"])

class usersAPI(Resource, userParams):

    """docstring for usersAPI"""

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('email', type=str, help="NO username")
        parser.add_argument('password', type=str, help="NO password")
        parser.add_argument('token', type=str, help='NO token')
        args = parser.parse_args()

        #args = self.reqparse.parse_args()
        user = User.query.filter(User.email==args['email']).first()
        if user and user.verify_passwd(args['password']):
            # return json.dumps(user.create_auth_token())
            token = str(user.create_auth_token())
            return {"token": token}
        else:
            return {"error": "Incorrect login or password"}


api = Api(blueprint)
api.add_resource(postAPI, "/app/post/<int:id>", endpoint="post")
api.add_resource(postsAPI, "/app/posts", endpoint="posts")
api.add_resource(
    articlesPageAPI, "/post/list/<int:page>/<int:per_page>", endpoint="articlesPage")
api.add_resource(userAPI, "/user/token", endpoint="userToken")
api.add_resource(usersAPI, "/users", endpoint="users")


@blueprint.route("/admin/")
def admin():
    return render_template("admin.html")

@blueprint.route("/app/")
def app():
    return render_template("app.html")
