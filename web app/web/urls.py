from django.urls import path
from . import views
from . import forms

urlpatterns = [
    # views
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("verify/", views.verify, name="verify"),
    path("login/", views.login, name="login"),
    path("setting/", views.setting, name="setting"),
    path("delete/", views.delete, name="delete"),
    path("task/", views.task, name="task"),
    path("game/", views.game, name="game"),
    path("out/", views.logout, name="out"),
    path("lang/<str:langcode>", views.change_language, name="change language"),
    path("robots.txt", views.robots, name="robots"),
    path("notfound/", views.notfound, name="404 error not found"),
    path("javascript/", views.javascript, name="javascript deactived"),
    # views with slash
    path("register", views.register, name="register"),
    path("verify", views.verify, name="verify"),
    path("login", views.login, name="login"),
    path("setting", views.setting, name="setting"),
    path("delete", views.delete, name="delete"),
    path("task", views.task, name="task"),
    path("game", views.game, name="game"),
    path("out", views.logout, name="out"),
    path("robots.txt", views.robots, name="robots"),
    path("notfound", views.notfound, name="404 error not found"),
    path("javascript", views.javascript, name="javascript deactived"),
    # forms
    path("register-form/", forms.registerform, name="register form"),
    path("login-form/", forms.loginform, name="login form"),
    path("verify-form/", forms.verifyform, name="verify form"),
    path("setting-form/", forms.settingform, name="setting form"),
    path("delete-form/", forms.deleteform, name="delete form"),
    path("game-form/", forms.startgameform, name="start game form"),
    path("complete-form/<str:result>", forms.completeform, name="complete a block"),
    # proccess
    path("image/", views.add_image_to_database, name="start game form"),
    path("getflag/<str:result>/", views.getflag, name="get red flag"),
    # proccess with slash
    path("image", views.add_image_to_database, name="start game form"),
    path("getflag/<str:result>", views.getflag, name="get red flag"),
]
