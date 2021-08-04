# Mercator
### Online shopping platform for both users and merchants

## Quick Overview
'**Mercator**' translated from latin meaning merchant is an online shop platform. *Users* would be able to browse, 
buy and review products as well as having the ability to open their own shop! Product recomendation is based on 
preferences and searches by the customer, optimizing the experience and shop sales.

*Merchants* can launch new products, manage the design, settings and analytics for their shop and grow their
brand. All customizable and with a lot of features!


## About the Project
This is my final project for Harvard's CS50Web course.**Researched**, **Planned**, **Designed** and **Developed** by me with 
the least amount of external packages allowing me to build my own systems, experiment and learn as much as 
possible.

### Why an online shop platform?
The specifications from the course discouraged the creation of an online shop since we already had a project 
on that topic, but I am personally interested in online shops and building a robust project like this one 
will be an innvaluable experience for me. Not to mention a challenge! 

I'm also aiming at specializing in this particular field, creating and maintaining virtual shops that allow 
brands to extend and open to larger markets and users easily finding the goods they need is a thrilling 
opportunity for me to take part, contribute and further develop the sector. Maybe even establishing new 
concepts and helping smaller bussinesses grow both on a local and if desired - global scale.

### What will Mercator provide?
My vision for the platform is to provide a lot of functionality for both regular customers and merchants. 
Browsing the shops and products will be available to all users with the following specifications:
- Browse collections of items from all shops
- Targeted product recommendations based on preferences and intrests/searches
- Detailed product views with images, categories, tags and specifications
- Select products to add to your cart
- Review products after making a purchase
- Apply your own preferences for products
- Manage the orders you places
- Edit your shipping information for orders
- **Open your own shop!**

After openning a shop you become a merchant, an extended version of a regular customer. This upgrade 
won't revoke any of your previous rights and you will become the owner of a brand new virtual shop!
These are the privilages you have:
- Managing the shop
    - Settings
    - Payment methods(2 supported)
    - Order enquiries
    - Product Creation
    - Shipment settings
- Custom styling(limited)
    - Uploading custom logo
    - Managing the background type
        - Solid color(default)
        - Background image/gif
    -Choosing between theme colors
- Analytics
    - track order and product performance
    - track individual page visits (Shop/Product)
    - monitor overall growth

Along with the features of the app, helper data models are required for better organisation and 
management of the project, whithout bloating everything in one place. Keeping it simple as much as 
possible! Here are the helper models(models with leading underscore are *private*):
- Image (for multiple arbitrary images on products)
- Shipment(Mainly details saved to each user's preferences)
- _ShopStyle:
    - background type selection
    - theme colors selection 
    - custom shop logo
- _ShopAnalytics: used mainly for grouping everything analytics related
    - Visit (each visit is stored as its own instance with a reference to analytics)
- ~~_ShopManagement~~ < all of these settings will go to the Shop model itself.

### How these features will be delivered/structured?
Since I will be using little to no 3rd party libraries, other than Django and Pillow(required for 
images), will require of me to write all of the bussines logic on my own and to handle configuration 
of more complex tasks. The structure of the webapp for managing different tasks:
- **pages** will be responsible for dynamicly generated pages, the core of the webapp 
- **users** - handling users, authentication, authorisation(on base level) and auth. templates
- **shop** - api that will be responsible for everything product and shop related

**Docker** will also be included and configured! < this was probably a mistake and not needed for my project
**PostgreSQL** set as the default database

### What i didn't use and why?
My first tought was to create a DRF backend and use React as frontend, tho this will
be the cleanest way for developing it is not what i want to showcase.
For the purpose of this course I will implement pretty much everything learned, 
dynamicly generated pages(Jinja), API, user auth, plain vanila JS without libraries or
frameworks, SCSS/CSS and testin. Possibly custom querries just as an experimentation
as well.

Most importantly, ***Tests***, a lot of them. Both unit and integration tests would be required!


## Live deployment of the project
~~After Mercator is finished, I will deploy the app(probably on Heroku) and configure it 
appropriately to serve static amd media(with *Cloudinary*) files, working with postgres, 
security and also experimenting with scalability(most likely not needed).~~

Just made a connection from GitHub to Heroku for CD(and proud about it). The docker container is running and you can browse the website but sadly the db is not configured
properly yet, a task for my next update.

The link is available here ***[mercator](http://mercator-val.herokuapp.com/)***

## Disclamer
As I develop the project there might be things that require change, removal or perhaps 
new features being included. This description is not complete and most certainly won't be 
the same on the last commit of this repository. 

I hope you are interested as much as I am in Mercator, cya on the finish line!
