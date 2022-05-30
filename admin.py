from flask_admin import Admin, AdminIndexView
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask import redirect, url_for, request

from app import app, db
from models import Client, MainPage, Role, User
from flask_admin.contrib.sqla import ModelView

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class AdminViewMix:
    """Class for overthrowing access to admin zone."""

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminViewMix, ModelView):
    pass


class HideAdminPage(AdminViewMix, AdminIndexView):
    pass


admin = Admin(app, 'Светлана Покровская', url='/', index_view=HideAdminPage(name='Home'))
admin.add_view(AdminView(Client, db.session))
admin.add_view(AdminView(MainPage, db.session))
