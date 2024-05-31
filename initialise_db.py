from project import db, create_app
from project.models import Photo, User
from werkzeug.security import generate_password_hash # (secure coding principles) password hashing

def populate_db():
    session = db.session()

    
    photos = [
        Photo(name='William Warby', caption='Gentoo penguin', description='A penguin with an orange beak standing next to a rock.', file='william-warby-_A_vtMMRLWM.jpg', user_id=1),
        Photo(name='Javier Patino Loira', caption='Common side-blotched lizard', description='A close up of a lizard on a rock.', file='javier-patino-loira-nortqDjv7ak.jpg', user_id=1),
        Photo(name='Jordie Rubies', caption='Griffin vulture flying', description='A large bird flying through a blue sky.', file='jordi-rubies-2wNkdL2oIyU.jpg', user_id=1),
        Photo(name='Jakub Neskora', caption='Jaguar', description='A close up of a leopard near a rock.', file='jakub-neskora-jloJvr74Fcc.jpg', user_id=1),
        Photo(name='William Warby', caption='Japanese macaque', description='A monkey sitting on top of a wooden post.', file='william-warby-ndWikw_TPfc.jpg', user_id=1),
        Photo(name='Ahmed Ali', caption='Berlin', description='An exciting part of Berlin. This place covers so many beautiful attractions in the city. From that spot you are already on the famous Oberbaumbrücke, you can see Molecule Man, and right behind me, you can see Berlin\'s beautiful skyline with the Fernsehturm right in the middle of it with the reflections of the spree.', file='ahmed-ali-Zl7bVVMEfg.jpg', user_id=1),
        Photo(name='Hanvin Cheong', caption='Nakano', description='A group of people walking across a street.', file='hanvin-cheong-9rBj8QYOL1Q.jpg', user_id=1),
        Photo(name='Ekaterina Bogdan', caption='Bologna', description='A bike parked next to a pole.', file='ekaterina-bogdan-BKJWsGB5h1s.jpg', user_id=1),
        Photo(name='Damian Ochrymowicz', caption='Nazare, Portugal', file='damian-ochrymowicz-GZQ7tKmEd9c.jpg', user_id=1),
        Photo(name='Dima DallAcqua', caption='Alcatraz Island', description='A close up of a green plant.', file='dima-dallacqua-U8TAGVPFJc4.jpg', user_id=1),
        Photo(name='Edgar', caption='Oporto, Portugal', description='A man sitting on a bench at a train station.', file='edgar-Q0g5Thf7Ank.jpg', user_id=1)
    ]

    for photo in photos:
        session.add(photo)
    session.commit()

    # creating users and setting an admin user 
    # (secure coding principles) hasing admin password
    admin_user = User(id=1, email='admin@mail.com', phone='01012345678', password=generate_password_hash('1234', method='pbkdf2:sha256', salt_length=8), is_admin=True)
    # (secure coding principles) hasing user password
    user = User(email='user@example.com', phone='01087654321', password=generate_password_hash('userpass', method='pbkdf2:sha256', salt_length=8))

    session.add(admin_user)
    session.add(user)
    session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()  
        db.create_all()  
        populate_db()