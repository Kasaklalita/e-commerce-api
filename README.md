
# E-commerce API with FastAPI

This API allows you to access a variety of e-commerce data, including products, businesses, and user information.


## Usage


The app is deployed, so you can just start testing it [here](https://jm5zb9.deta.dev/docs).

Some endpoints are available for everyone (like getting all of the products), but some need an authenticated user!

First of all, let\`s create a dummy account by trying out `POST /users`. Enter the required data and execute the query.

Once the user is created, you can log into your account by clicking a big green button "authorize" located on the top of the page.



More information on the user you have just created is available on `GET /users/me`. As you can see, your username and email are stored directly in the database, but the password is hashed.

The list of businesses is empty now, so let\`s create a few. Via trying out `POST /businesses/`, you can create businesses. Mind that all the names of the businesses must be unique. If you want a business to belong to your user, enter your user\`s ID (visit `GET users/me` to check your ID).

To ensure that your business has been successfully created, visit `GET /businesses/` to get all the businesses (you can specify the query parameters), or go to `GET /businesses/{id}` to get more information about a specific business (mind that `{id}` is the ID of the business).

Updating businesses is also available. Visit `PUT /businesses/{id}`. Enter the ID of the business as the query parameter, then specify all you need to update in the request body.

If you want to delete your business, go to `DELETE /businesses/{id}` and enter the ID of the business as the query parameter.

You can also create, read, update and delete products that belongs to businesses. These actions are performed similarly. Check out the `Products` section.

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
