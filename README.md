# SkillShelf

SkillShelf is a community-driven Django web application that helps users share skills and books, and provides an AI-powered study assistant.

## Features

- User Authentication
  - Register, login, and profile management
  - Extended user profiles with bio and location

- Skill Sharing & Matching
  - Add skills you can teach or want to learn
  - Automatic matching with compatible users
  - View and manage your skill matches

- Book Sharing & Digital Library
  - Add books to your collection
  - Browse and search available books
  - Send and manage borrow requests
  - Mark books for donation

- AI Study Assistant
  - Available for unmatched skills after 2 days
  - Get personalized learning roadmaps
  - Access recommended resources
  - Chat-based learning assistance

- Personal Dashboard
  - Overview of your skills and matches
  - Book collection and requests
  - Recent AI assistant sessions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arnii2511/Python_Mini_Project_SkillShelf.git
cd Python_Mini_Project_SkillShelf
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`.

## Usage

1. Register a new account or log in
2. Add skills you can teach or want to learn
3. Add books to your collection
4. Browse available skills and books
5. Send and manage borrow requests
6. Use the AI assistant for unmatched skills

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

 # SkillShelf
