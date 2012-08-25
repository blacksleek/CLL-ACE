# -*- coding: utf-8 -*-
import webapp2
from google.appengine.ext import db
from google.appengine.api import users

entry_open = """<html>
<head>
<title>文学 ACE!</title>
<link rel="icon" type="image/png" href="/Resource/images/favicon.png">
<link rel="stylesheet" href="/Resource/jquery.mobile-1.1.1.min.css" />
<link rel="stylesheet" href="/Resource/jqm-icon-pack-2.1.2-fa.css" />
<script src="/Resource/jquery-1.7.2.min.js"></script>
<script src="/Resource/jquery.mobile-1.1.1.min.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
</head>
<body align="center">"""

entry_close = """<br><br></body><div data-role="footer" data-position="fixed">&copy 文学 ACE! (v3.2)</div></html>"""

header_open = """<div data-role="header" data-position="fixed">
                <a href="/menu" data-role="button" data-rel="dialog" data-icon="list-ul" data-iconpos="notext"></a>
                <h1>"""

header_close = """</h1><a href="%s" data-ajax="false" data-role="button" data-icon="power" class="ui-btn-right">注销</a>
                                            </div>""" % users.create_logout_url("/")

class People(db.Model):
    name = db.StringProperty()

class Text(db.Model):
    name = db.ListProperty(str)
    comment = db.ListProperty(str)

class Feedback(db.Model):
    feedback = db.StringProperty()
    name = db.StringProperty()
    
class Entry(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/home")
        else:
            self.response.out.write(entry_open)
            self.response.out.write("""<div data-role="header" data-position="fixed">""" + """<h1>文学 ACE!</h1>""")
            self.response.out.write("""<a href="%s" class="ui-btn-right" data-role="button" data-ajax="false" data-inline="true" data-icon="power">登录</a></div>""" % users.create_login_url(self.request.uri))
            self.response.out.write("""<img src="/Resource/images/home_bg.png" />""")
            self.response.out.write(entry_close)

class Home(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write(entry_open)
            if People.get_by_key_name(user.email()):
                self.response.out.write(header_open)
                self.response.out.write(u"""主页 - """)
                self.response.out.write(People.get_by_key_name(user.email()).name)
            else:
                self.response.out.write(header_open)
                self.response.out.write(u"""主页 - """)
                self.response.out.write(user.email())
            self.response.out.write(header_close)
            self.response.out.write("""<img src="/Resource/images/home_bg.png" />""")
            self.response.out.write(entry_close)
        else:
            self.redirect("/error")

class Menu(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(u"""<div data-role="dialog" data-rel="back">
                                    <div data-role="header"><h1>菜单</h1>
                                    <div data-role="navbar">
                                    <ul>
                                    <li><a href="/home" data-ajax="false" data-icon="fahome">主页</a></li>
                                    <li><a href="/profile" data-ajax="false" data-icon="user">个人资料</a></li>
                                    <li><a href="/text" data-ajax="false" data-icon="book">文学读物</a></li>
                                    <li><a href="/oops" data-ajax="false" data-icon="comments">交易所</a></li>
                                    <li><a href="/feedback" data-ajax="false" data-icon="envelope-alt">反馈</a></li>
                                    <li><a href="/credits" data-ajax="false" data-icon="bookmark-empty">归功</a></li>
                                    </ul>
                                    </div></div></div>""")

class Profile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write(entry_open)
            if People.get_by_key_name(user.email()):
                self.response.out.write(header_open)
                self.response.out.write(u"""个人资料 - """)
                self.response.out.write(People.get_by_key_name(user.email()).name)
            else:
                self.response.out.write(header_open)
                self.response.out.write(u"""个人资料 - """)
                self.response.out.write(user.email())
            self.response.out.write(header_close)
            if People.get_by_key_name(user.email()):
                self.response.out.write(u"""<br><form action="/profile_update" method="post" data-ajax="false">
                                            用户名: <input type="text" name="name" value="%s" /><br>
                                            <input type="submit" value="更新" data-inline="true" />
                                            </form>""" % (People.get_by_key_name(user.email()).name))
            else:
                self.response.out.write(u"""<br><form action="/profile_update" method="post" data-ajax="false">
                                            用户名: <input type="text" id="name" name="name" />
                                            <input type="submit" value="更新" data-inline="true" />
                                            </form>""")
            self.response.out.write(entry_close)
        else:
            self.redirect("/error")

class Profile_Update(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        name = self.request.get("name")
        if user and People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            if name == People.get_by_key_name(user.email()).name:
                People(key_name = user.email(), name = name).put()
                self.redirect("/home")
            else:
                if name:
                    for i in People.all():
                        self.response.out.write(i.name)
                        if name == i.name:
                            self.response.out.write(header_open)
                            self.response.out.write(u"""个人资料 - """)
                            self.response.out.write(People.get_by_key_name(user.email()).name)
                            self.response.out.write(header_close)
                            self.response.out.write(u"""<br>用户名已被使用。<br>请另选用户名。<br>""")
                            self.response.out.write(u"""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
                    if len(name) > 16:
                        self.response.out.write(header_open)
                        self.response.out.write(u"""个人资料 - """)
                        self.response.out.write(People.get_by_key_name(user.email()).name)
                        self.response.out.write(header_close)
                        self.response.out.write(u"""<br>用户名不能超过16字符。<br>请另选用户名。<br>""")
                        self.response.out.write(u"""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
                    else:
                        if "<" in name and ">" in name:
                            name = name.replace("<", "&lt")
                            name = name.replace(">", "&gt")
                        People(key_name = user.email(), name = name).put()
                        self.redirect("/home")
                    
                    
                else:
                    self.response.out.write(header_open)
                    self.response.out.write(u"""个人资料 - """)
                    self.response.out.write(People.get_by_key_name(user.email()).name)
                    self.response.out.write(header_close)
                    self.response.out.write(u"""<br>请输入全部项目。<br>""")
                    self.response.out.write(u"""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
            self.response.out.write(entry_close)
        elif user:
            if name:
                for i in People.all():
                    if name == i.name:
                        self.response.out.write(entry_open)
                        self.response.out.write(header_open)
                        self.response.out.write(u"""个人资料 - """)
                        self.response.out.write(user.email())
                        self.response.out.write(header_close)
                        self.response.out.write("""<br>用户名已被使用。<br>请另选用户名。<br>""")
                        self.response.out.write("""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
                        self.response.out.write(entry_close)
                else:
                    if len(name) > 16:
                        self.response.out.write(header_open)
                        self.response.out.write(u"""个人资料 - """)
                        self.response.out.write(People.get_by_key_name(user.email()).name)
                        self.response.out.write(header_close)
                        self.response.out.write(u"""<br>用户名不能超过16字符。<br>请另选用户名。<br>""")
                        self.response.out.write(u"""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
                    else:
                        People(key_name = user.email(), name = name).put()
                        self.redirect("/home")
            else:
                self.response.out.write(entry_open)
                self.response.out.write(header_open)
                self.response.out.write(u"""个人资料 - """)
                self.response.out.write(user.email())
                self.response.out.write(header_close)
                self.response.out.write(u"""<br>请输入全部项目。<br>""")
                self.response.out.write("""<a href="/profile" data-role="button" data-ajax="false" data-inline="true">返回</a>""")
                self.response.out.write(entry_close)

        else:
            self.redirect("/error")

class Text_Page(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and People.get_by_key_name(user.email()):
                self.response.out.write(entry_open)
                self.response.out.write(header_open)
                self.response.out.write(u"""文学读物 - """)
                self.response.out.write(People.get_by_key_name(user.email()).name)
                self.response.out.write(header_close)
                self.response.out.write("""<div data-role="content"><div data-role="collapsible-set" data-theme="a">
                                            <div data-role="collapsible">
                                            <h1>唐诗</h1>
                                            <fieldset class="ui-grid-a">
                                                <div class="ui-block-a">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="A_Farewell_of_a_Friend" />
                                                <input type="text" style="display:none" name="title" value="《送友人》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《送友人》" /></form>
                                                </div>

                                                <div class="ui-block-b">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="A_Long_Climb" />
                                                <input type="text" style="display:none" name="title" value="《登高》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《登高》" /></form>
                                                </div>

                                                <div class="ui-block-a">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="A_Song_of_the_Yan" />
                                                <input type="text" style="display:none" name="title" value="《燕歌行》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《燕歌行》" /></form>
                                                </div>
                                                
                                                <div class="ui-block-b">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Untitled" />
                                                <input type="text" style="display:none" name="title" value="《无题》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《无题》" /></form>
                                                </div>
                                            </fieldset>
                                            
                                                <div data-inline="true">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Autumn_Evening_in_the_Mountains" />
                                                <input type="text" style="display:none" name="title" value="《山居秋暝》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《山居秋暝》" /></form>
                                                </div>
                                            </div>

                                            <div data-role="collapsible">
                                            <h1>宋词</h1>
                                            <fieldset class="ui-grid-a">
                                                <div class="ui-block-a">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Rain_Soaked_Bell" />
                                                <input type="text" style="display:none" name="title" value="《雨霖铃》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《雨霖铃》" /></form>
                                                </div>

                                                <div class="ui-block-b">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Charm_of_a_Maiden_Singer" />
                                                <input type="text" style="display:none" name="title" value="《念奴娇》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《念奴娇》" /></form>
                                                </div>

                                                <div class="ui-block-a">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Spring_in_Peach_Blossom_Land" />
                                                <input type="text" style="display:none" name="title" value="《武陵春》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《武陵春》" /></form>
                                                </div>
                                                
                                                <div class="ui-block-b">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Joy_of_Eternal_Union" />
                                                <input type="text" style="display:none" name="title" value="《永遇乐》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《永遇乐》" /></form>
                                                </div>
                                            </fieldset>
                                            
                                                <div data-inline="true">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Riverside_Daffodils" />
                                                <input type="text" style="display:none" name="title" value="《临江仙》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《临江仙》" /></form>
                                                </div>
                                            </div>
                                            
                                            <div data-role="collapsible">
                                            <h1>现代短片小说</h1>
                                            <fieldset class="ui-grid-b">
                                                <div class="ui-block-a">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Medicine" />
                                                <input type="text" style="display:none" name="title" value="《药》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《药》" /></form>
                                                </div>

                                                <div class="ui-block-b">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Most_Precious" />
                                                <input type="text" style="display:none" name="title" value="《最宝贵的》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《最宝贵的》" /></form>
                                                </div>

                                                <div class="ui-block-c">
                                                <form action="/Read" method="post" data-ajax="false">
                                                <input type"text" style="display:none" name="text" value="Line_of_Fate" />
                                                <input type="text" style="display:none" name="title" value="《命运的迹线》" />
                                                <input type="text" style="display:none" name="chapter" value="1" />
                                                <input type="submit" data-role="button" value="《命运的迹线》" /></form>
                                                </div>
                                            </fieldset>
                                            </div>
                                            
                                            <div data-role="collapsible">
                                            <h1>现代中篇小说</h1>
                                            <ul data-role="listview">
                                                <li><a href="/Fox_Volant_of_the_Snowy_Mountain" data-ajax="false">《雪山飞狐》</a></li>
                                            </ul>
                                            </div>
                                            
                                            </div></div>
                                            """)
                self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")

class Fox_Volant_of_the_Snowy_Mountain(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write("""《雪山飞狐》 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write("""<form action="/Read" method="post" data-ajax="false">
                                        <input type="text" style="display:none" name="text" value="Fox_Volant_of_the_Snowy_Mountain" />
                                        <input type="text" style="display:none" name="title" value="《雪山飞狐》" />
                                        <select name="chapter" data-native-menu="false">
                                            <option value="1">第一章</option>
                                            <option value="2">第二章</option>
                                            <option value="3">第三章</option>
                                            <option value="4">第四章</option>
                                            <option value="5">第五章</option>
                                            <option value="6">第六章</option>
                                            <option value="7">第七章</option>
                                            <option value="8">第八章</option>
                                            <option value="9">后记</option>
                                        </select>
                                        <input type="submit" data-role="button" value="阅读" />
                                        </form>""")
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")


class Read(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        title = self.request.get("title")
        text = self.request.get("text")
        chapter = self.request.get("chapter")
        if user and text and chapter and title:
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(title + """ - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write("""</h1><a href="%s" class="ui-btn-right" data-ajax="false" data-role="button" data-icon="power">注销</a>
                                        """ % users.create_logout_url("/"))
            self.response.out.write("""<form action="/Board" method="post" data-ajax="false">
                                        <input type="text" name="text" style="display:none" value="%s" />
                                        <input type="text" name="chapter" style="display:none" value="%s" />
                                        <input type="text" name="title" style="display:none" value="%s" />
                                        <fieldset class="ui-grid-a">
                                        <div class="ui-block-a" style="width:50%%">
                                        <input type="search" name="word" data-mini="true" />
                                        </div>
                                        <div class="ui-block-b" style="width:50%%">
                                        <input type="submit" value="%s" />
                                        </div>
                                        </fieldset>
                                        </form></div>""" % (text, chapter, title, u"论坛搜索"))
            
            text_name = text + " - " + chapter + ".txt"
            text_open = open(text_name, "r")
            contents = text_open.readlines()
            for line in contents:
                self.response.out.write(line +"""<br>""")
            if text == """A_Farewell_of_a_Friend""":
                self.response.out.write("""<br><br>在线朗读<br><audio src="/Resource/audio/A_Farewell_of_a_Friend_Audio.aac" controls></audio>""")
            if text == """A_Long_Climb""":
                self.response.out.write("""<br><br>在线朗读<br><audio src="/Resource/audio/A_Long_Climb_Audio.mp3" controls></audio>""")
            if text == """A_Song_of_the_Yan""":
                self.response.out.write("""<br><br>在线朗读<br><audio src="/Resource/audio/A_Song_of_the_Yan_Audio.mp3" controls></audio>""")
            if text == """Untitled""":
                self.response.out.write("""<br><br>在线朗读<br><audio src="/Resource/audio/Untitled_Audio.mp3" controls></audio>""")
            if text == """Autumn_Evening_in_the_Mountains""":
                self.response.out.write("""<br><br>在线朗读<br><audio src="/Resource/audio/Autumn_Evening_in_the_Mountains_Audio.mp3" controls></audio>""")
            self.response.out.write(entry_close)
            text_open.close()
        else:
            self.redirect("/error")

class Board(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        text = self.request.get("text")
        chapter = self.request.get("chapter")
        title = self.request.get("title")
        word = self.request.get("word")
        text_name = text + " - " + chapter + ".txt"
        text_open = open(text_name, "r")
        contents = text_open.readlines()
        for line in contents:
            if word.encode("utf-8") in line:
                break
        else:
            self.redirect("/not_found")
        if user and People.get_by_key_name(user.email()) and text and chapter and word:
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(word + """ - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            
            key_name = text + " - " + chapter + " - " + word
            if Text.get_by_key_name(key_name):
                if Text.get_by_key_name(key_name).name:
                    self.response.out.write("""<ul data-role="listview">""")
                    for i in range(0, len(Text.get_by_key_name(key_name).name)):
                        if Text.get_by_key_name(key_name).name[i] == user.email():
                            self.response.out.write(u"""<li>
                                                        <h4>%s</h4>
                                                        <p>%s</p>
                                                        <div align="right">
                                                        <form action="/Board_Delete" method="post" data-ajax="false">
                                                        <input type="text" style="display:none" name="key_name" value="%s" />
                                                        <input type="text" style="display:none" name="i" value="%s" />
                                                        <input type="text" style="display:none" name="text" value="%s" />
                                                        <input type="text" style="display:none" name="chapter" value="%s" />
                                                        <input type="text" style="display:none" name="word" value="%s" />
                                                        <input type="text" style="display:none" name="title" value="%s" />
                                                        <input type="submit" value="删除" data-mini="true" data-inline="true" />
                                                        </form>
                                                        </div>
                                                        </li>""" % (People.get_by_key_name(Text.get_by_key_name(key_name).name[i]).name, Text.get_by_key_name(key_name).comment[i], key_name, i, text, chapter, word, title))
                        else:
                            self.response.out.write("""<li>
                                                        <h4>%s</h4>
                                                        <p>%s</p>
                                                        </li>""" % (People.get_by_key_name(Text.get_by_key_name(key_name).name[i]).name, Text.get_by_key_name(key_name).comment[i]))

                    self.response.out.write("""</ul>""")
                else:
                    self.response.out.write(u"""<br>目前还没有能显示的帖子。<br>""")
                    self.response.out.write(u"""请帮忙发问第一个问题！""")
            else:
                self.response.out.write(u"""<br>目前还没有能显示的帖子。<br>""")
                self.response.out.write(u"""请帮忙发问第一个问题！""")
            self.response.out.write(u"""<div>
                                        <form action="/Board_Post" method="post" data-ajax="false">
                                        <input type="text" name="key_name" style="display:none" value="%s" />
                                        <input type="text" name="name" style="display:none" value="%s" />
                                        <input type="text" name="chapter" style="display:none" value="%s" />
                                        <input type="text" name="text" style="display:none" value="%s" />
                                        <input type="text" name="title" style="display:none" value="%s" />
                                        <input type="text" name="word" style="display:none" value="%s" />
                                        <input type="text" name="comment"><br>
                                        <input type="submit" value="发布" data-inline="true">
                                        </form>
                                        </div>""" % (key_name, user.email(), chapter, text, title, word))
            self.response.out.write(u"""<form action="/Read" method="post" data-ajax="false">
                                            <input type"text" style="display:none" name="text" value="%s" />
                                            <input type="text" style="display:none" name="title" value="%s" />
                                            <input type="text" style="display:none" name="chapter" value="%s" />
                                            <input type="submit" data-role="button" value="返回" data-inline="true" /></form>""" % (text, title, chapter))
            self.response.out.write(entry_close)
        elif People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""不适当 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br>请输入适当的词汇/句子。<br>""")
            self.response.out.write(u"""<form action="/Read" method="post" data-ajax="false">
                                            <input type"text" style="display:none" name="text" value="%s" />
                                            <input type="text" style="display:none" name="title" value="%s" />
                                            <input type="text" style="display:none" name="chapter" value="%s" />
                                            <input type="submit" data-role="button" value="返回" data-inline="true" /></form>""" % (text, title, chapter))
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")
                             
class Board_Post(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        key_name = self.request.get("key_name")
        name = self.request.get("name")
        comment = self.request.get("comment")
        chapter = self.request.get("chapter")
        text = self.request.get("text")
        title = self.request.get("title")
        word = self.request.get("word")
        if user and key_name and name and comment:
            if Text.get_by_key_name(key_name):
                if "<" in comment and ">" in comment:
                    comment = comment.replace("<", "&lt")
                    comment = comment.replace(">", "&gt")
                    t = Text.get_by_key_name(key_name)
                    t.name.append(name)
                    t.comment.append(comment)
                    t.put()
                    self.response.out.write(entry_open)
                    self.response.out.write(header_open)
                    self.response.out.write(u"""发布""" + """ - """)
                    self.response.out.write(People.get_by_key_name(user.email()).name)
                    self.response.out.write(header_close)
                    self.response.out.write(u"""<br>已发布此帖子: """)
                    self.response.out.write(comment)
                    self.response.out.write("""<br>""")
                    self.response.out.write(u"""<form action="/Board" data-ajax="false" method="post">
                                                <input type="text" name="chapter" style="display:none" value="%s" />
                                                <input type="text" name="text" style="display:none" value="%s" />
                                                <input type="text" name="title" style="display:none" value="%s" />
                                                <input type="text" name="word" style="display:none" value="%s" />
                                                <input type="submit" data-role="button" data-inline="true" value="返回" />
                                                </form>""" % (chapter, text, title, word))
                    self.response.out.write(entry_close)
            else:
                if "<" in comment and ">" in comment:
                    comment = comment.replace("<", "&lt")
                    comment = comment.replace(">", "&gt")
                    name_list = []
                    name_list.append(name)
                    comment_list = []
                    comment_list.append(comment)
                    Text(key_name = key_name, name = name_list, comment = comment_list).put()
                    self.response.out.write(entry_open)
                    self.response.out.write(header_open)
                    self.response.out.write(u"""发布 - """)
                    self.response.out.write(People.get_by_key_name(user.email()).name)
                    self.response.out.write(header_close)
                    self.response.out.write(u"""<br>已发布此贴子: """)
                    self.response.out.write(comment)
                    self.response.out.write("""<br>""")
                    self.response.out.write(u"""<form action="/Board" data-ajax="false" method="post">
                                                <input type="text" name="chapter" style="display:none" value="%s" />
                                                <input type="text" name="text" style="display:none" value="%s" />
                                                <input type="text" name="word" style="display:none" value="%s" />
                                                <input type="submit" data-role="button" data-inline="true" value="返回" />
                                                </form>""" % (chapter, text, word))
                    self.response.out.write(entry_close)
        else:
            self.redirect("/error")

class Board_Delete(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        key_name = self.request.get("key_name")
        i = self.request.get("i")
        i = int(i)
        i = i + 1
        text = self.request.get("text")
        chapter = self.request.get("chapter")
        word = self.request.get("word")
        title = self.request.get("title")
        if user and People.get_by_key_name(user.email()) and key_name and i:
            name_list = Text.get_by_key_name(key_name).name
            comment_list = Text.get_by_key_name(key_name).comment
            del(name_list[(i - 1)])
            del(comment_list[(i - 1)])
            Text(key_name = key_name, name = name_list, comment = comment_list).put()
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""删除 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br>帖子已删除。<br>""")
            self.response.out.write(u"""<form action="/Board" method="post" data-ajax="false">
                                        <input type="text" name="chapter" style="display:none" value="%s" />
                                        <input type="text" name="text" style="display:none" value="%s" />
                                        <input type="text" name="word" style="display:none" value="%s" />
                                        <input type="text" name="title" style="display:none" value="%s" />
                                        <input type="submit" data-inline="true" value="返回" /></form>""" % (chapter, text, word, title))
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")
            
class Feedback_Page(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""反馈 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br><form action="/feedback_post" method="post" data-ajax="false">
                                        <input type="text" name="feedback" />
                                        <input type="submit" value="发布反馈" data-inline="true" />
                                        </form>""")
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")

class Feedback_Post(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        feedback = self.request.get("feedback")
        if user and People.get_by_key_name(user.email()) and feedback:
            Feedback(name = user.email(), feedback = feedback).put()
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""反馈 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br>谢谢您的反馈。<br>
                                        <a href="/feedback" data-ajax="false" data-role="button" data-inline="true">返回</a>""")
            self.response.out.write(entry_close)
        elif user and People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""反馈 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br>请输入正确的反馈。<br>
                                        <a href="/feedback" data-ajax="false" data-role="button" data-inline="true">返回</a>""")
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")
            
class Credits(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user and People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""归功 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write(u"""<br><h2>读物摘自于：</h2><br>""")
            self.response.out.write("""<fieldset class="ui-grid-b">""")
            self.response.out.write("""<div class="ui-block-a"><a href="http://ds.eywedu.com/jinyong/xsfh/" data-role="button" data-ajax="false">《雪山飞狐》</a></div>""")
            self.response.out.write("""<div class="ui-block-b"><a href="http://www.5156edu.com/page/09-06-05/46774.html" data-role="button" data-ajax="false">《送友人》</a></div>""")
            self.response.out.write("""<div class="ui-block-c"><a href="http://www.laomu.cn/yingy/2009/200911/20091130104519_28679.html" data-role="button" data-ajax="false">《登高》</a></div>""")
            self.response.out.write("""<div class="ui-block-a"><a href="http://www.thn21.com/wen/show/27028.html" data-role="button" data-ajax="false">《燕歌行》</a></div>""")
            self.response.out.write("""<div class="ui-block-b"><a href="http://www.5156edu.com/page/09-06-26/47349.html" data-role="button" data-ajax="false">《无题》</a></div>""")
            self.response.out.write("""<div class="ui-block-c"><a href="http://www.laomu.cn/yingy/2009/200911/20091130104253_28674.html" data-role="button" data-ajax="false">《山居秋暝》</a></div>""")
            self.response.out.write("""<div class="ui-block-a"><a href="http://www.millionbook.com/mj/l/luxun/lh/007.htm" data-role="button" data-ajax="false">《药》</a></div>""")
            self.response.out.write("""<div class="ui-block-b"><a href="http://www.millionbook.com/xd/w/wangmeng/000/008.htm" data-role="button" data-ajax="false">《最宝贵的》</a></div>""")
            self.response.out.write("""<div class="ui-block-c"><a href="http://www.hkreporter.com/talks/thread-1177838-1-1.html" data-role="button" data-ajax="false">《命運的跡線》</a></div>""")
            self.response.out.write("""<div class="ui-block-a"><a href="http://zhidao.baidu.com/question/2580787.html" data-role="button" data-ajax="false">《雨霖铃》</a></div>""")
            self.response.out.write("""<div class="ui-block-b"><a href="http://longyusheng.org/ci/sushi/22.html" data-role="button" data-ajax="false">《念奴娇》</a></div>""")
            self.response.out.write("""<div class="ui-block-c"><a href="http://www.diyifanwen.com/sicijianshang/songdai/liqingzhao/0673004200675618.htm" data-role="button" data-ajax="false">《武陵春》</a></div>""")
            self.response.out.write("""<div class="ui-block-a"><a href="http://www.zk168.com.cn/shiyong/jianshang/songdai_117853.html" data-role="button" data-ajax="false">《永遇乐》</a></div>""")
            self.response.out.write("""<div class="ui-block-b"><a href="http://longyusheng.org/ci/yanjidao/1.html" data-role="button" data-ajax="false">《临江仙》</a></div>""")
            self.response.out.write("""</fieldset>""")
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")

class Not_Found(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if People.get_by_key_name(user.email()):
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write("""未找到 - """)
            self.response.out.write(People.get_by_key_name(user.email()).name)
            self.response.out.write(header_close)
            self.response.out.write("""<br>在读物里未找到所输入的词汇/句子。<br>""")
            self.response.out.write("""请勿输入间距。""")
            self.response.out.write(entry_close)
        elif user:
            self.redirect("/visit_profile")
        else:
            self.redirect("/error")

class Visit_Profile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write(entry_open)
            self.response.out.write(header_open)
            self.response.out.write(u"""个人资料 - """)
            self.response.out.write(user.email())
            self.response.out.write(header_close)
            self.response.out.write(u"""<br>请更新个人资料。<br>""")
            self.response.out.write(entry_close)
        else:
            self.redirect("/error")
        
class Error(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(entry_open)
        self.response.out.write(header_open)
        self.response.out.write(u"""故障""")
        self.response.out.write(header_close)
        self.response.out.write(u"""<br>您没有权限浏览此页。""")
        self.response.out.write(entry_close)

class Oops(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(entry_open)
        self.response.out.write(header_open)
        self.response.out.write(u"""抱歉！""")
        self.response.out.write(header_close)
        self.response.out.write(u"""<br>抱歉，此页还未开发。<br>""")
        self.response.out.write(u"""我们将会尽快完成。""")
        self.response.out.write(entry_close)

app = webapp2.WSGIApplication([('/', Entry),
                               ('/home', Home),
                               ('/menu', Menu),
                               ('/profile', Profile),
                               ('/text', Text_Page),
                               ('/Fox_Volant_of_the_Snowy_Mountain', Fox_Volant_of_the_Snowy_Mountain),
                               ('/Read', Read),
                               ('/Board', Board),
                               ('/Board_Post', Board_Post),
                               ('/Board_Delete', Board_Delete),
                               ('/feedback', Feedback_Page),
                               ('/feedback_post', Feedback_Post),
                               ('/credits', Credits),
                               ('/profile_update', Profile_Update),
                               ('/not_found', Not_Found),
                               ('/visit_profile', Visit_Profile),
                               ('/error', Error),
                               ('/oops',Oops)],
                               debug=True)
