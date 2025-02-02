import re
import json
import hashlib
import firebase_admin
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.animation import Animation
from firebase_admin import credentials, db
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFillRoundFlatIconButton, MDRectangleFlatButton, MDFlatButton


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "collect-62f2a",
  "private_key_id": "0ac2b25401fd1f408f1daec92b2ae005081c3cc4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCy+49G7tFonPhJ\nyKUos8Oyl9h4LWJTRnZPwi9EQprv3fpHCl1fYsqNAz4SAGeFIM+Ny44nmxfS7044\nh9dPrg3fFiZGxsD/aa1bwxk1Ku1Pk1GUmj4nlFcO4rTDU2whItyltYgzMg5Ljjzi\nuWYelW3LW/GnpGoBiTgDVXBlOma00NXxvStlZRjjq4UKaUSUhitcXor+VSbZE7db\nM/O2sagA7Jxf0rAkcRuCaZNxsvXwt3Qx/Ivsv6cxAONN1XaxTSYRwglrnX2+TJOD\ni+zbPNqQ7XtP/7bYNvRdEmEQxhj7v2bFBT7w3jYiajeOCaddKIaRxPAj2EAanjLJ\nUqz+RDnLAgMBAAECgf9T5ZdDqK6AWxQHggXpDlqtXIAb1SpB3sWWnW+Kj64QwfyP\nUEx0adqIPvzZc1cTEE46KTB5YDnKpmIEHajPsMbPy5IlmwTctKyOVuV6BqU2p9eV\n0LdR1jb4w0v4QyJsZesHwhAV72DECeiAXmd/7ouIx5B/BJKsJaYb6fDFgpqiJnhA\nO+tZZnP0xK3ymg23/mdRUUlxdQV6PIbl+nV8TISv+0NluiYOrXpyR5OYrTkDs1Kw\navJaR/zBKouw2OJy/MMuQ+sJBFViahWKmvtdw+ZibXZOqrS6j9Y/oguUtBh+SCm0\npcidOAUD3Rx5TNE0ho4oihCZR4lZmwP8sdrrKQECgYEA7t9O/c9tHDuKZPIX39dL\nmVLuXGGVDPoPf0QZFil5wWz8wE4/gHW3ezGH5TfhGUew4F3gp3r11zUPCjeJ2s6C\nE7Lb5h5251kW64h2J2jAWKq6WO1/ciwEbnABPTPcpAA1f2FpTTGF7vUSf65Ui/Jk\nhQ9JIjdIk4bSMOgn6I0OVzECgYEAv9Dt0Juv4CnKb6JidR9C18XEOcoYtb53aN6P\nb8MRfhLe5e1UJ5vlSJWqKjlHlMkwhjKHVgA8SYIEaFNS6i/d0gMbQqkFzQF7Dnmd\nMCygNMeiZRVtCjqPLt0hlHkuaeVmXuHhTOwjueDKphZL8/BvLvvhum31yRnk09C3\n52aC2bsCgYEApsUbRhJaT/q1vZJT3sBWFH6U0cSDJmMzDJxDk3hze/qWX8CBjzMg\nXY8QHJUtv9OQhqSkIumy14RAstZhlXTV1eDqq7ebNhu558kHDK6Sk5Tmsw1lDBX1\nJhFmnA8oPQu0TfF5bh5kLpfFSYUxm98oFMm+Ong0YGMhPmnm6vIIEBECgYEAosjq\nqjkV/0U4GZlTuVX4YiniJ7ENW1/y8rq+O/juJXJaXAMXgi3ZXco2CXNm/ivn1FuZ\nYzD7+N4wY2EjYr+QnqQoRGAxHhP9nQE0lyeoJmKtvN98FEwyK3FbCCf3bcNTJ37G\nt4NHpn3RPTZ66uDHWrZEkPS0vCAPhHsDN4xVy/UCgYBZGkxIqbhd2S6JmnWICG/7\nOj/BIrc0XNOijsWadXhUXPtZiuoQdtczgC9O/eoGTqdesInXPzz6GoxFJ1ZmshP+\n7JRlVCQ5ixaGXKS6RGilFIU2tCW6O54a7nWAaDkUrLRtgPmgsd4n4zfxnQ2qnbS7\n74ql32C/Z45Hj+X0DfL80Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-6odu7@collect-62f2a.iam.gserviceaccount.com",
  "client_id": "108220296849664319898",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-6odu7%40collect-62f2a.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://collect-62f2a-default-rtdb.asia-southeast1.firebasedatabase.app/ '
})

def hash_password(password):
    """Hash the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Validate the email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.credentials_file = "credentials.json"
        self.logged_in_email = "logged_in.json"

        self.result_card = MDCard(
            size_hint=(None, None),
            size=("280dp", "140dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            padding="16dp",
            orientation="vertical",
            ripple_behavior=True,
            md_bg_color=(0.1, 0.6, 0.6, 1),
            opacity=0,
        )
        self.card_label = MDLabel(
            text="Character: None\nPoints: 0",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
        )
        self.result_card.add_widget(self.card_label)
        self.add_widget(self.result_card)

        self.email_input = MDTextField(
            hint_text="Enter your email",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            size_hint=(0.8, None),
            height="40dp",
        )
        self.add_widget(self.email_input)

        password_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.8, None),
            height="40dp",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        self.password_input = MDTextField(
            hint_text="Enter your password",
            password=True,
            size_hint=(0.85, None),
            pos_hint={"center_x":0.5, "center_y":0.2},
            max_text_length=6
        )
        password_layout.add_widget(self.password_input)

        self.eye_icon_button = MDIconButton(
            icon="eye-off",
            size_hint=(None, None),
            size=("40dp", "40dp"),
            pos_hint={"center_y": 0.1},
        )
        self.eye_icon_button.bind(on_release=self.toggle_password_visibility)
        password_layout.add_widget(self.eye_icon_button)

        self.add_widget(password_layout)

        self.login_button = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.login_button.bind(on_release=self.handle_login)
        self.add_widget(self.login_button)

        self.create_account_button = MDRaisedButton(
            text="Create Account",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )
        self.create_account_button.bind(on_release=self.handle_create_account)
        self.add_widget(self.create_account_button)

    def load_logged_in_email(self):
        """Load the logged-in email from the file."""
        try:
            with open(self.logged_in_email, "r") as file:
                data = json.load(file)
                return data.get("email", None)
        except (FileNotFoundError, KeyError):
            return None


    def toggle_password_visibility(self, instance):
        """Toggle password visibility."""
        if self.password_input.password:
            self.password_input.password = False
            self.eye_icon_button.icon = "eye"
        else:
            self.password_input.password = True
            self.eye_icon_button.icon = "eye-off"

    def handle_login(self, instance):
        """Handle login logic."""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            self.show_message("Please enter email and password!")
            return

        hashed_password = hash_password(password)
        ref = db.reference("users")
        user_data = ref.child(email.replace(".", ",")).get()

        if user_data and user_data.get("password") == hashed_password:
            self.save_logged_in_email(email)
            self.manager.current = "game"
            self.manager.transition.direction = 'left'
            self.manager.get_screen("account").update_email_label(email)  
            self.manager.get_screen("game").redeem_code_input.text=''
            self.manager.get_screen("game").result_card.opacity=0
            self.result_card.opacity=0
            self.email_input.text = ''
            self.password_input.text = ''
        else:
            self.show_message("Invalid email or password!")

    def handle_create_account(self, instance):
        """Handle account creation logic."""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        user_name = "Not set"
        user_age = "Not set"
        user_id = "Not set"


        if not email or not password:
            self.show_message("Please enter email and password!")
            return

        hashed_password = hash_password(password)
        ref = db.reference("users")
        email_key = email.replace(".", ",")

        if ref.child(email_key).get():
            self.show_message("Account already exists!")
        else:
            ref.child(email_key).set({
            "password": hashed_password,
            "user_name": user_name,
            "user_age": user_age,
            "user_id": user_id,
            "points": 0,
            "used_codes": {}
        })
            self.save_logged_in_email(email)
            self.manager.current = "game"
            self.manager.transition.direction = 'left'
            self.manager.get_screen("account").update_email_label(email) 
            self.manager.get_screen("game").result_card.opacity=0
            self.result_card.opacity=0
            self.email_input.text = ''
            self.password_input.text = ''

    def load_credentials(self):
        """Load credentials from the file line by line."""
        credentials = {}
        try:
            with open(self.credentials_file, "r") as file:
                for line in file:
                    entry = json.loads(line.strip())
                    credentials.update(entry)
        except FileNotFoundError:
            pass
        return credentials

    def save_credentials(self, credentials):
        """Save each email and hashed password on a new line."""
        with open(self.credentials_file, "w") as file:
            for email, password in credentials.items():
                json.dump({email: password}, file)
                file.write("\n")


    def save_logged_in_email(self, email):
        """Persist logged-in email."""
        with open("logged_in.json", "w") as file:
            json.dump({"email": email}, file)


    def show_message(self, message):
        self.card_label.text = message
        anim = Animation(opacity=1, d=0.5)
        anim.start(self.result_card)



class redeemCodeGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data_file = "user_data.json"
        self.logged_in_email = None
        self.load_user_data()

        self.points_label = MDLabel(
            text="Points: 0",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.93},
            theme_text_color="Primary",
            font_style="H6",
        )
        self.add_widget(self.points_label)

        self.redeem_code_input = MDTextField(
            hint_text="Enter redeem code",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            size_hint=(0.8, None),
            height="40dp",
        )
        self.add_widget(self.redeem_code_input)

        self.submit_button = MDRaisedButton(
            text="Submit",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        self.submit_button.bind(on_release=self.check_redeem_code)
        self.add_widget(self.submit_button)


        self.account_button = MDIconButton(
            icon="account-circle",
            size_hint= (0.15,None), 
            pos_hint={"center_x": 0.9, "center_y": 0.05},
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1,1,1,1),
            theme_text_color='Custom',
        )
        self.account_button.bind(on_release=self.go_account)
        self.add_widget(self.account_button)

        self.redeem_button = MDIconButton(
            icon="gift-outline",
            size_hint= (0.15,None), 
            pos_hint={"center_x": 0.1, "center_y": 0.07},
            md_bg_color=(0,150/255, 136/255, 1),
            text_color=(1,1,1,1),
            theme_text_color='Custom',
        )
        self.add_widget(self.redeem_button)

        self.result_card = MDCard(
            size_hint=(None, None),
            size=("280dp", "140dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding="16dp",
            orientation="vertical",
            ripple_behavior=True,
            md_bg_color=(0.1, 0.6, 0.6, 1),
            opacity=0,
        )
        self.card_label = MDLabel(
            text="Character: None\nPoints: 0",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
        )
        self.result_card.add_widget(self.card_label)
        self.add_widget(self.result_card)

    def on_enter(self):
        """Load logged-in user email and update points."""
        login_screen = self.manager.get_screen("login")
        self.logged_in_email = login_screen.load_logged_in_email()

        if self.logged_in_email:
            email_key = self.logged_in_email.replace(".", ",")
            ref = db.reference("users")
            user_data = ref.child(email_key).get()

            if user_data:
                points = user_data.get("points", 0)
                self.update_points_label(points)
            else:
                self.update_points_label(0)
        else:
            self.update_points_label(0)



    def load_user_data(self):
        try:
            with open(self.user_data_file, "r") as file:
                self.user_data = json.load(file)
        except FileNotFoundError:
            self.user_data = {}

    def save_user_data(self):
        with open(self.user_data_file, "w") as file:
            json.dump(self.user_data, file, indent=4)

    def update_points_label(self, new_points):
        """Update the points label with the latest points."""
        self.points_label.text = f"Points: {new_points}"


    def check_redeem_code(self, instance):
        """Check the redeem code and update points."""
        redeem_code = self.redeem_code_input.text.strip()

        if not self.logged_in_email:
            self.show_message("No user logged in!")
            return

        email_key = self.logged_in_email.replace(".", ",")
        ref = db.reference("users")
        user_data = ref.child(email_key).get()

        if not user_data:
            self.show_message("User data not found!")
            return

        if "used_codes" not in user_data:
            user_data["used_codes"] = {}

        if redeem_code in user_data["used_codes"]:
            self.show_message("Code already used!")
            return

        predefined_codes = {
            "Iron3000": {"character": "Iron Man (Infinity war)", "points": 3000},
            "Cap": {"character": "Captain America (The Avenger)", "points": 1000},
            "Thorlove": {"character": "Thor (Thor Love and Thunder)", "points": 1500},
            "Hulk": {"character": "Hulk (The Avenger)", "points": 2000},
            "Widow": {"character": "Black Widow (Black Widow)", "points": 2000},
            "CapMarvel": {"character": " Captain Marvel (The Captain Marvel)", "points": 1000},
            "Spidy": {"character": "Spiderman (Far From Home)", "points": 3000},
            "Panther": {"character": "Black Panther (Black Panther)", "points": 2000},
            "Strange": {"character": "Doctor Strange (Infinty War)", "points": 3000},
            "Wanda": {"character": "Scarlet Witch (Wanda Vision)", "points": 1000},
            "Vision": {"character": "Vision (Age of Ultorn)", "points": 1000},
            "Ant": {"character": "Antman (Antman)", "points": 1500},
            "Falcon": {"character": "Falcon (Civil War)", "points": 1500},
            "Bucky": {"character": "Winter Soldier (Captain America the Winter Soldier)", "points": 1500},
            "Loki": {"character": "Loki (Loki)", "points": 10000},
            "Stark": {"character": "Tony Stark (The Avenger)", "points": 2000},
            "Fury": {"character": "Nick Fury (The Avenger)", "points": 300},
            "Hawk": {"character": "Hawkeye (The Avenger)", "points": 500},
            "Villain": {"character": "Thanos (Infinity War)", "points": 10000},
            "Ultron": {"character": "Ultron (Age of Ultron)", "points": 1000},
            "Red": {"character": "Red Skull (Captain America)", "points": 1000},
            "Hela": {"character": "Hela (Thor Ragnarok)", "points": 2000},
            "Kill": {"character": "Killmonger (Black Panther)", "points": 1500},
            "No Death": {"character": "Deadpool (Deadpool and Wolverine)", "points": 9000},
            "Wolverine": {"character": "Wolverine (Deadpool and Wolverine)", "points": 6000},
            "she": {"character": "She-Hulk (She-Hulk)", "points": 100},
            "Venom3": {"character": "Venom (Venom The Last Dance)", "points": 2000},
            "Groot": {"character": "Groot (Guardians of the Galaxy)", "points": 500},
            "Rocket": {"character": "Rocket (Guardians of the Galaxy)", "points": 1500},
            "Gamora": {"character": "Gamora (Guardians of the Galaxy)", "points": 500},
            "Star": {"character": "Star Lord (Guardians of the Galaxy)", "points": 1500},
            "Drax": {"character": "Drax (Guardians of the Galaxy)", "points": 100},
            "Mantis": {"character": "Mantis (Guardians of the Galaxy)", "points": 500},
            "Nebula": {"character": "Nebula (Guardians of the Galaxy)", "points": 100},
            "Marvel's Flash": {"character": "Makkari (Eternals)", "points": 2000},
        }

        if redeem_code in predefined_codes:
            character = predefined_codes[redeem_code]["character"]
            points = predefined_codes[redeem_code]["points"]

            user_data["used_codes"][redeem_code] = {"character": character, "points": points}
            new_points = user_data.get("points", 0) + points

            ref.child(email_key).update({
                "points": new_points,
                "used_codes": user_data["used_codes"]
            })

            self.update_points_label(new_points)
            self.show_message(f"Character: {character}\nPoints: {points}")
        else:
            self.show_message("Invalid redeem code!")




    def show_message(self, message):
        """Display a message in the result card and automatically hide it after a few seconds."""
        self.card_label.text = message
        anim = Animation(opacity=1, d=0.5)
        anim.start(self.result_card)

        Clock.schedule_once(self.hide_message, 3)

    def hide_message(self, *args):
        """Hide the result card."""
        anim = Animation(opacity=0, d=0.5)
        anim.start(self.result_card)

    def go_account(self, instance):
        self.manager.current="account"
        self.manager.transition.direction = 'left'
        


class accountscreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logged_in_email = self.load_logged_in_email()
        self.user_data_file = "user_data.json"

        self.account_icon = Image(
            source="account-circle.png",
            size_hint=(None, None),
            size=("150dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.85},
        )
        self.add_widget(self.account_icon)

        email_card = MDCard(
            size_hint=(0.95, None),
            height="50dp",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            md_bg_color=(0.2, 0.6, 0.8, 1),
            radius=[10, 10, 10, 10],
        )

        entry_card = MDCard(
            size_hint=(0.95, None),
            height="120dp",
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            md_bg_color=(0.9, 0.9, 0.9, 1),
            radius=[10, 10, 10, 10],
        )

        self.email_label = MDLabel(
            text=self.logged_in_email if self.logged_in_email else "No user logged in",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
        )
        email_card.add_widget(self.email_label)
        self.add_widget(email_card)

        self.entry = MDLabel(
            text=f"User Name:   \n \nAge:   \n \nUser ID:   ",
            size=("50px", "50px"),
            bold=True,
            padding="10px",
        )
        entry_card.add_widget(self.entry)
        self.add_widget(entry_card)


        self.edit_button=MDIconButton(
            icon='account-edit',
            md_bg_color=(0.5,0.5,0.5,1),
            pos_hint={"center_x" : 0.9, "center_y":0.3},
            icon_color=(1,1,1,1),
            theme_icon_color='Custom',
        )
        self.edit_button.bind(on_release=self.change_to_edit)
        self.add_widget(self.edit_button)

        self.logout_button = MDFlatButton(
            text="Logout",
            pos_hint={"center_x": 0.1, "center_y": 0.25},
            theme_text_color='Custom',
            text_color='red'
        )
        self.logout_button.bind(on_release=self.handle_logout)
        self.add_widget(self.logout_button)

        self.account_button = MDIconButton(
            icon="account-circle",
            size_hint= (0.15,None), 
            pos_hint={"center_x": 0.9, "center_y": 0.07},
            md_bg_color=(0.4, 0.4, 0.4, 1),
            text_color=(1,1,1,1),
            theme_text_color='Custom',
        )
        self.add_widget(self.account_button)

        self.redeem_button = MDIconButton(
            icon="gift-outline",
            size_hint= (0.15,None), 
            pos_hint={"center_x": 0.1, "center_y": 0.05},
            md_bg_color=(0, 150/255, 136/255, 1),
            text_color=(1,1,1,1),
            theme_text_color='Custom',
        )
        self.redeem_button.bind(on_release=self.change_to_redeem)
        self.add_widget(self.redeem_button)


    def load_logged_in_email(self):
        """Load the logged-in email from the file."""
        try:
            with open("logged_in.json", "r") as file:
                data = json.load(file)
                return data.get("email", None)
        except (FileNotFoundError, KeyError):
            return None

    def update_email_label(self, email):
        """Update the email label with the logged-in email."""
        self.email_label.text = f"{email}"

    def handle_logout(self, instance):
        """Handle user logout."""
        try:
             # Clear logged-in email from file
            with open("logged_in.json", "w") as file:
                json.dump({"email": None}, file)
                
        except Exception as e:
            print(f"Error clearing logged-in user: {e}")

        self.manager.current = "login"
        self.manager.transition.direction = 'right'


    def change_to_edit(self, instance):
        self.manager.current = "edit"
        self.manager.transition.direction = 'left'

    def change_to_redeem(self, instance):
        self.manager.current = "game"
        self.manager.transition.direction = 'right'

    def on_enter(self):
        """Load user data when the account screen is entered."""
        login_screen = self.manager.get_screen("login")
        self.logged_in_email = login_screen.load_logged_in_email()

        if self.logged_in_email:
            email_key = self.logged_in_email.replace(".", ",")
            ref = db.reference("users")
            user_data = ref.child(email_key).get()

            if user_data:
                username = user_data.get("user_name", "Not set")
                age = user_data.get("user_age", "Not set")
                user_id = user_data.get("user_id", "Not set")
                points = user_data.get("points", 0)
                self.entry.text = (
                    f"User Name: {username}\n \n"
                    f"Age: {age}\n \n"
                    f"User ID: {user_id}"
                )
            else:
                self.entry.text = "User data not found."
        else:
            self.entry.text = "No user logged in."

class editscreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.user_data_file = "user_data.json"

        self.message_card = MDCard(
            size_hint=(None, None),
            size=("280dp", "30dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            padding="16dp",
            orientation="vertical",
            ripple_behavior=True,
            md_bg_color=(1, 0, 0, 1),
            opacity=0,
        )
        self.message_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
        )
        self.message_card.add_widget(self.message_label)
        self.add_widget(self.message_card)

        self.back_to_account=MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x":0.1, "center_y":0.95},
        )
        self.back_to_account.bind(on_release=self.to_account)
        self.add_widget(self.back_to_account)

        self.user_name_input=MDTextField(
            hint_text="Enter User Name",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            size_hint=(0.8, None),
            height="40dp",
            mode='rectangle',
        )
        self.add_widget(self.user_name_input)


        self.age=MDTextField(
            hint_text='Enter Your Age',
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            size_hint=(0.8, None),
            height='40dp',
            mode='rectangle',
            input_filter='int',
            max_text_length=3,
        )
        self.add_widget(self.age)

        self.user_id_input=MDTextField(
            hint_text="Enter User ID",
            pos_hint={'center_x':0.5, 'center_y': 0.5},
            size_hint=(0.8, None),
            height='40dp',
            mode='rectangle',
        )
        self.add_widget(self.user_id_input)


        self.save_button=MDRaisedButton(
            text="Save",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            size_hint=(0.3, 0.05)
        )
        self.save_button.bind(on_release=self.save_user_name)
        self.add_widget(self.save_button)

    def to_account(self, instance):
        self.manager.current="account"
        self.manager.transition.direction = 'right'
        
    def save_user_name(self, instance):
        """Save user data to Firebase."""
        username = self.user_name_input.text.strip()
        user_id = self.user_id_input.text.strip()
        age = self.age.text.strip()

        if not username or not user_id or not age:
            self.show_message("Please fill in all fields!")
            return

        try:
            age = int(age)
        except ValueError:
            self.show_message("Age must be a number!")
            return

        login_screen = self.manager.get_screen("login")
        logged_in_email = login_screen.load_logged_in_email()

        if logged_in_email:
            email_key = logged_in_email.replace(".", ",")
            ref = db.reference("users")
            ref.child(email_key).update({
                "user_name": username,
                "user_age": age,
                "user_id": user_id
            })

            account_screen = self.manager.get_screen("account")
            account_screen.on_enter()

            self.manager.current = "account"
            self.show_message("Details saved successfully!")
            self.user_name_input.text = ''
            self.age.text = ''
            self.user_id_input.text = ''
        else:
            self.show_message("No user logged in!")


    def show_message(self, message):
        self.message_label.text = message
        anim = Animation(opacity=1, d=0.5)
        anim.start(self.message_card)

        Clock.schedule_once(self.hide_message, 3)

    def hide_message(self, *args):
        """Hide the result card."""
        anim = Animation(opacity=0, d=0.5)
        anim.start(self.message_card)



class Collecteber(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        sm = ScreenManager()

        login_screen = LoginScreen(name="login")
        sm.add_widget(login_screen)
        sm.add_widget(redeemCodeGame(name="game"))
        sm.add_widget(accountscreen(name="account"))
        sm.add_widget(editscreen(name="edit"))

        logged_in_email = login_screen.load_logged_in_email()
        if logged_in_email:
            sm.current = "game"
        else:
            sm.current = "login"

        return sm



if __name__ == "__main__":
    Collecteber().run()