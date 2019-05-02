from flask.cli import FlaskGroup

from app import create_app
from app.database import db
from app.api.user.models import User


app = create_app()
cli = FlaskGroup(create_app=create_app)
prompt = "> "

@cli.command('create_admin')
def create_admin_user():
    if not User.check4admin():
        print("Username? ")
        username = input(prompt)
        
        print("Email")
        email = input(prompt)

        print("Password")
        pw1 = input(prompt)

        print("Password Wiederholung")
        pw2 = input(prompt)

        if not (pw1 == pw2):
            print("Passwörter stimmen nicht überein, bitte wiederholen Sie den Vorgang")
        else:
            user = User(username, pw1, email)
            user.is_admin = True
            user.save()
            print("Admin wurde angelegt")

    else:
        print("Es existiert bereits ein Admin")

if __name__ == '__main__':
    cli()
