#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from validate import Validation
from google.appengine.ext import ndb
from logging import debug
import cgi
import os
import time
import webapp2
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       extensions=['jinja2.ext.autoescape'])



# MODELS #
class Users(ndb.Model):
    # Model for Users #
    user = ndb.StringProperty()
    password = ndb.StringProperty()
    link = ndb.StringProperty()
    tagline = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class Subject_Main(ndb.Model):
    # Top level subject for forums #
    subject = ndb.StringProperty()
    subject_id = ndb.IntegerProperty()


class ForumPost(ndb.Model):
    # Model for Forum Posts #
    subject = ndb.StringProperty()
    subject_id = ndb.IntegerProperty()
    poster = ndb.StringProperty()
    post = ndb.StringProperty()
    tag = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    avatar = ndb.StringProperty()


class Definitions(ndb.Model):
    # Model for word entries #
    word = ndb.StringProperty()
    definition = ndb.StringProperty()


# custom #
class SetUser(object):
        # Sets current user info #
        def __init__(self, **kwargs):
            Base.current_user = kwargs['user']
            Base.current_tag = kwargs['tagline']
            Base.current_avatar = kwargs['avatar']
            Base.login = True


# HANDLERS #
class Handler(webapp2.RequestHandler):
    # Class for Handling templates #
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, ** params):
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))


class Register(Handler):
    # register user into database, check for possible invalid entries #
    error = False

    def get(self):
        # any errors flagged? #
        if Register.error is False:
            self.render("register.html")
        else:
            # show error flag, then reset #
            self.render("register.html", error=Register.error,
                        username=Base.current_user, avatar=Base.current_avatar,
                        tagline=Base.current_tag)
            Register.error = False

    def post(self):
        # gather registration info #
        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))
        avatar = self.request.get('avatar')
        tagline = cgi.escape(self.request.get('tagline'))

        # Run Validation #
        validate = Validation('register', username=username,
                              password=password, avatar=avatar,
                              tagline=tagline)
        validate.run_validation()
        if self.check_user(username):
            # check if username is duplicate #
            self.redirect('/register.html')
        elif validate.error_return():
            # set error flag if any #
            Register.error = validate.error_return()
            self.redirect('/register.html')
        elif not Register.error:
            # set user as active #
            SetUser(user=username, avatar=avatar, tagline=tagline)
            # add user info to database. #
            new_user = Users(user=username,
                             password=password,
                             link=avatar,
                             tagline=tagline)
            new_user.put()
            time.sleep(.2)
            self.redirect('/forum.html')

    def check_user(self, user):
        # checks if username is already in DB #
        check = Base.query_users.fetch()
        for field in check:
            debug('User being checked --{}'.format(field.user))
            if user == field.user:
                # set error flag #
                Register.error = '*{}* is unavailable as a username.'.format(user)
                return Register.error
        return Register.error


class Definition(Handler):
    # shows definitions and allows user to enter in new entries does not have to be registered #
    error = False

    def get(self):
        word_list = Definitions.query().order(Definitions.word).fetch()
        if Definition.error:
            self.render("definitions.html", wordlist=word_list, login=Base.login,
                        user=Base.current_user, u_image=Base.current_avatar,
                        error=Definition.error)
        else:
            self.render("definitions.html",  wordlist=word_list, login=Base.login,
                        user=Base.current_user, u_image=Base.current_avatar)

    def post(self):
        word = cgi.escape(self.request.get('word'))
        definition = cgi.escape(self.request.get('definition'))
        # validate information #
        validate = Validation('', word=word, definition=definition)
        validate.run_validation()

        if not validate.error_return():
            # looks good now add to DB #
            define = Definitions(word=word, definition=definition)
            define.put()
            time.sleep(.2)
            Base.login = True
            self.redirect('/definitions.html')
        else:
            # set error flag #
            Definition.error = validate.error_return()
            self.redirect('definitions.html')


class NotesData(Handler):
    # Notes Handler #
    def get(self):
        user = Base.current_user
        self.render("notes.html", login=Base.login,
                    user=user, u_image=Base.current_avatar,)


class ForumPage(Handler):
    # Allows registered user to enter in a post, does not allow for blank posts #
    error = False

    def get(self):
        posts = ForumPost.query().order(ForumPost.date).fetch()
        subjects = Subject_Main.query().order(Subject_Main.subject_id).fetch()
        total_posts = len(posts)
        if ForumPage.error is False:
            # looks good process page #
            debug('Total posts = {}'.format(total_posts))
            self.render("/forum.html",
                        post_list=posts,
                        subjects=subjects,
                        login=True,
                        user=Base.current_user,
                        u_image=Base.current_avatar,
                        total_posts=total_posts)

        else:
            # errors on page so will show error flag #
            self.render("/forum.html",
                        post_list=posts,
                        subjects=subjects,
                        login=True,
                        user=Base.current_user,
                        u_image=Base.current_avatar,
                        error=ForumPage.error,
                        total_posts=total_posts)
            # error being shown, so reset error flag #
            ForumPage.error = False

    def post(self):
        # get current registered user and post #

        # test to see if subject has already been posted #
        # if so add current post under that subject title and unique_id #
        # and update the current Base unique_id #

        if self.request.get('subject_id') == '':
            debug(' New subject_id  ')
            subject_id = Base().set_post_id()
        else:
            debug(' Found subject_id ')
            subject_id = self.request.get('subject_id')

        subject = cgi.escape(self.request.get("subject"))
        post = cgi.escape(self.request.get("post"))
        poster = Base.current_user
        tag = Base.current_tag
        avatar = Base.current_avatar
        debug('....POSTING...')

        if post:
            # looks good add post to database #
            subject_add = Subject_Main(subject=subject, subject_id=int(subject_id))
            subject_add.put()
            debug('--Subject added--')
            forum_post = ForumPost(subject_id=int(subject_id),
                                   subject=subject,
                                   post=post,
                                   poster=poster,
                                   tag=tag,
                                   avatar=avatar)
            forum_post.put()
            debug('Post added--')
            # for local #
            time.sleep(.2)
            Base.login = True
            self.redirect('/forum.html')
        else:
            # set error flag #
            ForumPage.error = 'Can not post a blank post..'
            self.redirect('/forum.html')


class MainPage(Handler):
    # MainPage (index.html) Handler #
    error = ''

    def get(self):
        # test to see if registered user is or is not logged in #
        latest_post = ForumPost.query().order(-ForumPost.date).fetch(1)
        if Base.login is False:
            self.render("index.html", login=False, latest_post=latest_post, error=MainPage.error)
        else:
            self.render("index.html",
                        login=True,
                        user=Base.current_user,
                        u_image=Base.current_avatar,
                        latest_post=latest_post)

    def post(self):

        # get user name and password and check for invalid characters #
        qualify_user = cgi.escape(self.request.get("username"))
        qualify_pass = cgi.escape(self.request.get("password"))

        # if user has valid creds then set login flag and user info#
        if self.check_creds(qualify_user, qualify_pass):
            self.render("index.html", login=True,
                        user=Base.current_user, u_image=Base.current_avatar)
        else:
            # no creds did not validate, set error flag #
            MainPage.error = 'You\'ve entered the wrong name or password..'
            self.render("index.html", login=False, error=MainPage.error)

    def check_creds(self, user, password):
        # qualify user against user info in database#
        for fields in Base.query_users:
            if str(fields.user) == str(user) and \
               str(fields.password) == str(password):
                SetUser(user=fields.user,
                        tagline=fields.tagline,
                        avatar=fields.link,
                        )
                return True


class Base(Handler):
    # Base Template Handler #
    query_users = Users.query()
    subj_unique_id = 1000
    # Initialize base user info #
    login = False
    current_user = ''
    current_tag = ''
    current_avatar = ''

    navs_list ={'HOME': '/', 'FORUM': 'forum.html',
                'NOTES': 'notes.html', 'DEFINITIONS': 'definitions.html',
                'REGISTER': 'register.html', 'DICE': 'dice.html'}

    def get(self):
        self.render("base.html", login=Base.login)

    def post(self):
        pass

    def set_post_id(self):
        # sets unique id #
        # get latest post #
        post_id = ForumPost.query().order(-ForumPost.date).fetch(1)
        # check to see if there is a subject_id #
        if post_id[0].subject_id >= 1000:
            p_id = post_id[0].subject_id
            p_id += 1
            debug('post_id {}'.format(p_id))
            return p_id
        # if not set to default of subj_unique_id #
        # should only run once !! #
        else:
            p_id = Base.subj_unique_id
            return p_id


router = [('/', MainPage),
          ('/notes.html', NotesData),
          ('/definitions.html', Definition),
          ('/register.html', Register),
          ('/forum.html', ForumPage),
          ('/base.html', Base),
          ]
app = webapp2.WSGIApplication(router, debug=True)

