from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Example debug session
if __name__ == "__main__":
    alice = Author("Alice")
    alice.save()

    mag = Magazine("Tech Monthly", "Tech")
    mag.save()

    alice.add_article(mag, "AI in 2024")
    print(alice.articles())
    print(alice.magazines())
