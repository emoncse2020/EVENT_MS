import os
import django
from faker import Faker
import random
from events.models import Participant, Category, Event 
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_ms.settings') 
django.setup()

fake = Faker()

def create_categories(n=5):
    """Create fake categories."""
    categories = []
    for _ in range(n):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.text()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")
    return categories

def create_participants(n=10):
    """Create fake participants."""
    participants = []
    for _ in range(n):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()  # Ensures unique emails
        )
        participants.append(participant)
    print(f"Created {len(participants)} participants.")
    return participants

def create_events(n=10, categories=None, participants=None):
    """Create fake events and assign them to categories and participants."""
    if categories is None:
        categories = list(Category.objects.all())
    if participants is None:
        participants = list(Participant.objects.all())

    events = []
    for _ in range(n):
        event = Event.objects.create(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )
        event.participants.set(random.sample(participants, random.randint(1, min(5, len(participants)))))  # Assign 1-5 participants
        events.append(event)
    
    print(f"Created {len(events)} events.")
    return events

def populate_database():
    """Populate the database with fake data."""
    print("Starting database population...")

    categories = create_categories(5)
    participants = create_participants(20)
    create_events(10, categories, participants)

    print("Database populated successfully!")

# Run the script
if __name__ == "__main__":
    populate_database()
