import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
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

        INSERT INTO authors (id, name) VALUES (1, 'Alice Smith');
        INSERT INTO magazines (id, name, category) VALUES (1, 'Tech Weekly', 'Technology');
        INSERT INTO magazines (id, name, category) VALUES (2, 'Nature Today', 'Science');
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('AI Revolution', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Green Future', 1, 2);
    """)
    conn.commit()
    conn.close()

def test_save_author():
    author = Author("New Author")
    author.save()
    assert author.id is not None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (author.id,))
    row = cursor.fetchone()
    assert row["name"] == "New Author"

def test_find_by_id():
    author = Author.find_by_id(1)
    assert author is not None
    assert author.name == "Alice Smith"
    assert author.id == 1

def test_articles_returns_all_by_author():
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) == 2
    titles = [a["title"] for a in articles]
    assert "AI Revolution" in titles
    assert "Green Future" in titles

def test_magazines_returns_unique_magazines():
    author = Author.find_by_id(1)
    magazines = author.magazines()
    names = [m["name"] for m in magazines]
    assert sorted(names) == sorted(["Tech Weekly", "Nature Today"])

def test_add_article_creates_new_article():
    author = Author("Bob Builder")
    author.save()

    magazine = Magazine("Builder Digest", "Engineering")
    magazine.save()

    author.add_article(magazine, "How to Build Robots")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE title = ?", ("How to Build Robots",))
    article = cursor.fetchone()

    assert article is not None
    assert article["author_id"] == author.id
    assert article["magazine_id"] == magazine.id

def test_topic_areas_returns_unique_categories():
    author = Author.find_by_id(1)
    topics = author.topic_areas()
    assert sorted(topics) == sorted(["Technology", "Science"])

