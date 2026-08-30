# Udemy FastAPI TDD Tutorial

## Links

- [Try FastAPI Test Driven Development](https://www.udemy.com/course/try-fastapi-api-test-driven-development/)
- [diagrams 1.drawio on Google Drive](https://drive.google.com/file/d/1jB-kxVXzDNjHxa8J8yso9h7Jk7pkaOXF/view?usp=sharing)
- [Database ERD](https://lucid.app/lucidchart/dcf7e614-f071-4832-99b6-361b13db1a9f/edit?viewport_loc=-956%2C-904%2C2725%2C1479%2C0_0&invitationId=inv_12607d3e-7a85-4489-83fd-0aa57812706f)
- [FastAPI docs](https://pypi.org/project/fastapi/)
- [The Twelve-Factor App](https://12factor.net/)

## PyTest

- [Fixtures reference](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [Reflecting DB objects](https://docs.sqlalchemy.org/en/21/core/reflection.html#sqlalchemy.engine.reflection.Inspector.has_table)

## SQL

```SQL
select tc.constraint_name, tc.constraint_type
from information_schema.table_constraints tc
where tc.table_name = 'categories' and tc.constraint_type = 'CHECK';
```

```SQL
select tc.constraint_name, tc.constraint_type
from information_schema.table_constraints tc
where tc.table_name = 'categories' and tc.constraint_type = 'UNIQUE';
```

## Tools

- [Whiteboard.office.com](https://whiteboard.office.com)
