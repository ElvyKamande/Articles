import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;

        INSERT INTO authors (id, name) VALUES (1, 'Jane Doe');
        INSERT INTO magazines (id, name, category) VALUES (1, 'Nature News', 'Science');
    """)
    conn.commit()
    conn.close()

def test_save_article():
    article = Article("The Cosmos Explained", 1, 1)
    article.save()

    assert article.id is not None

    # Check that it was saved correctly
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row["title"] == "The Cosmos Explained"
    assert row["author_id"] == 1
    assert row["magazine_id"] == 1

def test_find_by_id():
    article = Article("Black Holes and Beyond", 1, 1)
    article.save()

    fetched = Article.find_by_id(article.id)
    assert fetched is not None
    assert fetched.title == "Black Holes and Beyond"
    assert fetched.author_id == 1
    assert fetched.magazine_id == 1
