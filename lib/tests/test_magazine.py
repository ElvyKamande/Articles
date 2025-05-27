import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;

        INSERT INTO magazines (id, name, category) VALUES (1, 'Tech Monthly', 'Technology');
        INSERT INTO authors (id, name) VALUES (1, 'Jane Doe');
        INSERT INTO authors (id, name) VALUES (2, 'John Smith');

        INSERT INTO articles (title, author_id, magazine_id) VALUES ('AI Trends', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Quantum Tech', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Cybersecurity Today', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Gadget Review', 2, 1);
    """)
    conn.commit()
    conn.close()

def test_save_magazine():
    mag = Magazine("Health Weekly", "Health")
    mag.save()
    assert mag.id is not None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM magazines WHERE id = ?", (mag.id,))
    row = cursor.fetchone()
    assert row["name"] == "Health Weekly"
    assert row["category"] == "Health"

def test_find_by_id():
    mag = Magazine.find_by_id(1)
    assert mag is not None
    assert mag.name == "Tech Monthly"
    assert mag.category == "Technology"


