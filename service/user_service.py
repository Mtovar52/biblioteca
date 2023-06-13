from db.entity.user_entity import User 
from repository.repo_user import Users_repository
from service.validate.bcrypt import Bcrypt

class Service_users:
    user_repo = Users_repository()
    
    def create_user(self, user:User): 
        bcrypt = Bcrypt()
        hash = bcrypt.generate_password(user.password)

        new_user =  {
            "name" : user.name,
            "email" : user.email,
            "password" : hash
        }
        response = self.user_repo.create_user(new_user)
    
        return response
        
    def get_user(self, email:str): 
       response = self.user_repo.get_user(email)
       return response

    
    