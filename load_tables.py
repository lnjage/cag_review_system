import csv
from app import create_app, db
from app.models import User, Abstract, Review

app = create_app()

def load_abstracts_from_csv(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            abstract = Abstract(
                email=row['email'],
                title=row['title'],
                subject=row['subject'],
                
                content=row['content']
            )
            db.session.add(abstract)
        db.session.commit()
    print("Abstracts loaded successfully.")

def assign_reviews():
    abstracts = Abstract.query.all()
    reviewers = User.query.filter_by(is_admin=False).all()

    for abstract in abstracts:
        subject = abstract.subject.lower()
        eligible_reviewers = [r for r in reviewers if subject in r.subjects.lower()]
        assigned = []

        while len(assigned) < 3 and eligible_reviewers:
            reviewer = eligible_reviewers.pop()
            if reviewer not in assigned:
                review = Review(abstract_id=abstract.id, reviewer_id=reviewer.id)
                db.session.add(review)
                assigned.append(reviewer)
    db.session.commit()
    print("Reviews assigned successfully.")

with app.app_context():
    load_abstracts_from_csv('sample_abstracts.csv')
    assign_reviews()
