from werkzeug.security import generate_password_hash, check_password_hash


class Bcrypt:
    def verify_password(self, plain_password, hashed_password):
        return check_password_hash(hashed_password, plain_password)

    def generate_password(self, password):
        return generate_password_hash(password, "pbkdf2:sha256:30", 30)