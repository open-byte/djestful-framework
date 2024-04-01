# ruff: noqa: F401
# type: ignore
from djestful import operation

class UserView(APIView, prefix='user'):
    tags = ['User']
 
    @operation.get(path='user/{id}')
    def get(self, id: int) -> User:
        return User.objects.get(id=id)

    @operation.post(path='user')
    def post(self, user: User) -> User:
        user.save()
        return user

    @operation.put(path='user/{id}')
    def put(self, id: int, user: User) -> User:
        user.id = id
        user.save()
        return user

    @operation.delete(path='user/{id}')
    def delete(self, id: int) -> None:
        User.objects.get(id=id).delete()
        return None




@operation.get(path='user')
def get_users(self) -> List[User]:
    return User.objects.all()


# Path: urls.py
# Compare this snippet from urls.py:
from django.urls import path
    
urlpatterns = [
    path('', UserView.as_view(), name='user'),
]

# type: ignore
# ruff: noqa: F401
