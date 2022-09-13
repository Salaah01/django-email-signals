# Change Log

### 1.0.8 Fixed bug relating to CSS files not loading in admin
- A bug where CSS files were not loading in the admin page has been resolved.

### 1.0.7 Fixed bug relating to multiple signals for the same model
- When retrieving signal constraints we were previously filtering by a signal's content type using the `Signal.objects.get` method. However, there can been multiple `Signal` instances for a single content type. This therefore would cause an error. This has been fixed by retrieving the signal constraints from the `Signal` instance directly.

### 1.0.6 Ability to add email list
- `mailing_list` now accepts a comma separated list of email addresses as well as a function that would return a list of email addresses.

### 1.0.5 - setup.cfg requirements fixed
- Fixed Django requirement in setup.cfg

## 1.0.4 - Ability to add context to plain and HTML fields.
- Added the ability to add context to the plain and HTML fields.

## 1.0.3 - Bug fixes
- Fixed bug where certain fields could not be accessed in a model when saving signal constraints.
- Allowed `created` as a valid value for `param_1` in the signal constraints form.

## 1.0.2 - Supports Grapelli
- Now supports [django-grapelli](https://django-grappelli.readthedocs.io/en/latest/).

## 1.0.1 - Ckeditor
- Added Ckeditor

## 1.0.0 - Initial Release
- Initial Release
