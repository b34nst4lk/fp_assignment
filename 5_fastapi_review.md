# FastAPI

## Introduction

FastAPI is a web framework built upon Starlette and Pydantic. As it is a library 
intended to be packaged and served from repositories like PyPI, the top level 
folder contains the module itself (named `fastapi`) and all support tests and 
documentation.

## Starting at the top

The top level folder is structured as such.
```
.
├── CONTRIBUTING.md
├── docs                # documentation with internationalization
├── docs_src            # code examples used in docs
├── fastapi             # main module 
├── LICENSE
├── pyproject.toml
├── README.md
├── scripts             # Utility scripts for testing, building and publishing the library and documentation
├── SECURITY.md
└── tests               # test cases for fastapi
``` 

When the library is installed by a user, only the `fastapi` folder is actually 
installed. 

### docs and docs_src

Both modules combined together provide the documentation in various languages
and the code examples used. Code examples are written in code and not within
the documentation itself so that they can be tested.

### tests

Tests are broken down into individual use cases. For example, tests related to 
how path params are handled are stored in `test_path.py`. The reason would
likely be to ensure that the use cases a user may require is grouped together 
so that they are easy to find.


### fastapi module

Within the fastapi module, we have the following submodules,
```
./fastapi
├── dependencies
├── middleware
├── openapi
├── security
```
and everything else as .py files.

The submodules organizes serveral high level concepts used by fastapi together.
The dependencies module facilitates the use of dependency injection in
the http operations, middleware handles pre and post-processing for every
requests and response, openapi is responsible for all the ingredients necessary
to generate OpenAPI documentation, and security contains all of the common ways
that security is implemented.

Comparing the .py files with how [Starlette]'s library is structured, we do 
see many similarities. For example, both Starlette and FastAPI have an 
`applications.py`, but FastAPI subclasses from Starlette. Others include 
`templating.py`, where FastAPI simply imports from Starlette.

In `fastapi.__init__.py`, we do see that exports are restricted through the 
declaration of `__all__`. Classes and functions listed here are what provides 
the core functionality of this library.

## Potential imporvements to structure of code

For it's given purpose as a framework, with many users and contributors, I 
believe that the libaray structure is currently at its best possible structure 
for the following reasons.

1. At the top level of the code base, we see that everything related to 
   managing and testing the repo are consolidated together, and they don't 
   affect the behavior of the core libaray. 

3. Tests are structured and titled such that browsing the folder already 
   provides a high level overview of what each set of tests are about.
   
5. In the `fastapi` module, the titles of files are essentially what you would 
   expect out of most libaray frameworks. Files like `applications.py` and 
   `routing.py` give sufficient clues on what they are trying to accomplish and 
   how they should be used.

If I have to identify a possible improvement in the structure, I would say that having
only imports in a single file should just be imported in the `__init__.py` and exposed
in the `__all__` declaration, as they merely expose the imported libary. 

However, this sacrifices the clarity that the current structure has. Every 
step of a request lifecycle has it's own file. While `templating.py`, for example,
merely imports from Starlette, and may seem redundant initially, having it as a
discrete file clearly shows any maintainer or user that this is where templating
is done, and any extensions associated with templating should be done here.

[Starlette]: <> (https://github.com/encode/starlette/tree/master/starlette)
