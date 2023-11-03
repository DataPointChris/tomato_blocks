# Tomato Blocks

1. Create Data Model
  1. The `TomatoBlock` is doing too much.  There should be a way to start and cancel a `TomatoBlock` and it will save the state to the database.
  2. Printing and display should be somewhere else.
2. Make the metrics part of their own module and import it
3. Set up pre-commit hooks, borrow from ichrisbirch
4. Put a pre-commit hook in templates
5. Figure out something to do with templates, standards, reference. (blue book or mkdocs)
6. Update SQLALCHEMY
7. Update SQLAlchemy syntax to new select
8. Change session to be a generator used in a with block
9.  Does sqlalchemy handle connection pooling?
