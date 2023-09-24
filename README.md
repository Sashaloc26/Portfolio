1)store

An online clothing store  where the user can register and log in using GitHub, make an order and track the status of the order.
- Authorization via django-allauth
- Email to confirm registration using EmailBackend
- Redis page caching
- Optimization of registration speed using Celery workers
- Updated users profiles, order basket, tracking order status, restrictions for unauthorized users.
- FrontEnd(HTML,CSS,Bootstrap)
- Unit Testing
- Code checked with PEP 8 standards using flake8 linter

Stack:Django,PostgreSQL,Redis,Celery,Unit-Tests,HTML,CSS,Bootstrap,flake8


2)drfproj

An online library where authorized users can: like and rate books, mark the book that has been read.
- Authorization using Python Social Auth
- Implemented API on Django Rest Framework
- Solved the n+1 problem and optimized database queries
- CRUD service with filters, sorting search
- Test coverage more than 90% Unit-Testing
- Relationships between users and books in the form of: likes, ratings and marks.
- Code checked for PEP 8 standards using flake8 linter

Stack:Django,Django Rest Framework,PostgreSQL,Unit Testing, flake8

3)recipe_help

Website with recipes and functionality for searching for recipes based on your available products or receiving a random recipe when interacting with the interface.
-Implemented a small visualization of the project using djangotemplates
-Caching the main page using redis
-Tests with Unit Testing

Stack:Django,PostgreSQL,Redis,Unit Testing,HTML,CSS
