"""
Phase 3 Code Challenge: Articles – Magazine Domain (no SQLAlchemy)

This single file implements the three classes and all required deliverables:
- Author
- Magazine
- Article

Design goals:
- Simple, test-friendly OOP with class registries (for Articles and Magazines).
- Property validations that only set values if they pass constraints.
- Methods match the required names exactly (articles, magazines, contributors, etc.).
- No exceptions by default (to match the base tests). See notes at bottom for the Bonus.

How to use in your project layout (typical Flatiron/Moringa structure):
- Save this file as `lib/magazine.py` (or adjust imports in tests accordingly).
- Optional: create `lib/debug.py` that imports these classes and plays with them.

Author: jared kiprop
"""
from __future__ import annotations
from typing import List, Optional, ClassVar


class Article:
    """An Article belongs to one Author and one Magazine; has a title.

    - title: str, 5..50 chars, immutable after first set
    - author: Author, can be changed after init
    - magazine: Magazine, can be changed after init

    Class keeps a registry of all Article instances for convenience.
    """

    _all: ClassVar[List["Article"]] = []

    def __init__(self, author: "Author", magazine: "Magazine", title: str) -> None:
        # set order: title first (immutable), then author/magazine via setters
        self._title: Optional[str] = None
        self.title = title  # will only set if valid

        self._author: Optional[Author] = None
        self.author = author

        self._magazine: Optional[Magazine] = None
        self.magazine = magazine

        # add to registry if core fields are valid
        Article._all.append(self)

    # -------------------- title (immutable after first valid set) --------------------
    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        # Only allow setting once (hint used: hasattr-like via _title None check)
        if self._title is not None:
            return  # do not allow changes after first set
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        # else: keep None; base tests typically don't require raising.

    # -------------------- author (changeable) --------------------
    @property
    def author(self) -> Optional["Author"]:
        return self._author

    @author.setter
    def author(self, value: "Author") -> None:
        from_types_ok = (value is not None) and isinstance(value, Author)
        if from_types_ok:
            self._author = value
        # else: ignore invalid assignment

    # -------------------- magazine (changeable) --------------------
    @property
    def magazine(self) -> Optional["Magazine"]:
        return self._magazine

    @magazine.setter
    def magazine(self, value: "Magazine") -> None:
        from_types_ok = (value is not None) and isinstance(value, Magazine)
        if from_types_ok:
            self._magazine = value
        # else: ignore invalid assignment

    # -------------------- class helpers --------------------
    @classmethod
    def all(cls) -> List["Article"]:
        return list(cls._all)


class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Immutable after first set
        if hasattr(self, "_name"):
            return  # ignore future changes
        if isinstance(value, str) and len(value) > 0:
            self._name = value

    def articles(self):
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        return list({m.category for m in self.magazines()})


class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # else ignore invalid assignment

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # else ignore invalid assignment

    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        return list({a.author for a in self.articles()})

    def article_titles(self):
        if not self.articles():
            return None
        return [a.title for a in self.articles()]

    def contributing_authors(self):
        authors = [a.author for a in self.articles()]
        return list({a for a in authors if authors.count(a) > 2}) or None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.title = title
        self.author = author
        self.magazine = magazine
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Immutable after first set
        if hasattr(self, "_title"):
            return  # ignore reassignment
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
