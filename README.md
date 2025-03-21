# Mizuhara

---

### Create Your Telegram Bot More Easily.(Draft)

---

#### 1. Introduction

When you create a telegram bot with python, you may face with PyTelegramBotAPI or python-telegram-bot.
You may recognise that it is not easy to handler both two packages to create your own telegram bot.
These package are not a framework, so you have to design all structure from the scratch. 
You have to all functions to message or callback handlers as a minimum, 
additionally you may have to create another global variables to control telegram bot more precisely.
If you have any experience to write a code with python packages related with telegram, 
you might be frustrated that your code is so verbose and seems not to be able to be done maintenance.

This project, which is called Mizuhara(the origin of water), was started to solve the difficulties during producing telegram bot.
Mizuhara is mimic Django Rest API Framework(DRF), so you have to set the route, view as well as serializers.
Only difference between Mizuhara and Django is, the previous one does not provide any models, which are charge of defining table of database.


