# 50k Push-up Challenge

A companion web app to log and track progress to completing 50k push-ups (or however many your goal is) during 2025.

## Design/development ideas 

- Easy input of push-ups done
   - preset multiples of 10?
   - Remember and default to the latest amount entered?
- Show today's progress **DONE**
   - and other time periods?
- Show total progress **DONE**
   - towards today's goal (in order to reach the full goal) **DONE**
- Set your own end goal amount (if not 50k)
- Add "backlog" entries, i.e. set date (& time?) for the entry.
- Option to record sets and reps, not only total reps, for an entry. **DONE**

- Use sqlite in lieu of Postgres? **DONE**
- Use HTMX 
- Use django-components?

## MVP TARGETS
- Ability to set date & time when adding log entry **DONE**
- Remove sets **DONE**
- Ability to delete entry **DONE**
- Ability to set own goal(?)

## Documentation

[Django 4.2](https://docs.djangoproject.com/en/4.2/)  
[Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)  
[Django-Bootstrap5 23.3](https://django-bootstrap5.readthedocs.io/en/latest/index.html)  
[Environs 9.5.0](https://pypi.org/project/environs/)  
[Whitenoise 6.5.0](https://whitenoise.readthedocs.io/en/latest/index.html)  
[Pytest-Django 4.5.2](https://pytest-django.readthedocs.io/en/latest/)  
[Mailhog 1.0.1](https://github.com/mailhog/MailHog#readme)


# Features 

* Setup to use with Visual Studio Code [Dev containers](https://code.visualstudio.com/docs/devcontainers/containers) and Github [Codespaces](https://github.com/features/codespaces)
    - With Postgres and Mailhog configured out of the box
* Barebones HTML template based on [Bootstrap 5](https://getbootstrap.com/) using [Django-Bootstrap5](https://github.com/zostera/django-bootstrap5)
    - With horizontal/collapsable navbar from scratch
* Configuration with env variables using [environs\[django\]](https://github.com/sloria/environs)
* Barebones extended user model
    - With login/logout functionality prepared and integrated in navbar
* [Whitenoise](https://github.com/evansd/whitenoise) for serving static files
* Testing with [pytest](https://docs.pytest.org/en/7.4.x/) using [pytest-django](https://github.com/pytest-dev/pytest-django)
* [Github Dependabot](https://github.com/dependabot) configuration out of the box


## TODO

* User registration
* Password reset
* Mail config
* CI/CD support?
* Skeleton HTML/CSS/JS setup [DONE]?
    * With templates and stuff
* Production Docker config [DONE]
    (See https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
    * Gunicorn/Nginx [DONE]
    * SSL/Let's Encrypt [DONE]
* Whitenoise [DONE]
* Django-Bootstrap5 [DONE]
* Configured for PostgreSQL [DONE]
* Settings from enviroment variables [DONE]
    * Django settings URL [DONE]
* Extended User model [DONE] (?)
    (See https://testdriven.io/blog/django-custom-user-model/)
    * Add login page [DONE]
    * Add user/login link to top navigation [DONE]
    * Add tests with pytest! [DONE]

### Development environment

* Testing with pytest [DONE]
* Dev container [DONE]
* Django Debug Toolbar [DONE]
* Mailhog [DONE]
