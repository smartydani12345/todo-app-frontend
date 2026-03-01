from database.session import SessionLocal
from models.user import User, utc_now
from auth.utils import hash_password

session = SessionLocal()
try:
    hashed = hash_password('Test123!')
    print('Password hashed:', hashed[:20], '...')

    now = utc_now()
    user = User(
        name='Script Test',
        email='script2@example.com',
        password_hash=hashed,
        created_at=now,
        updated_at=now
    )
    print('User object created')

    session.add(user)
    print('User added to session')

    session.commit()
    print('Session committed, User ID:', user.id)
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
finally:
    session.close()
