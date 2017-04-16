# Angular and Angular Material Helper for Django

[![Travis]][Travis Link] [![Code Climate]][Code Climate Link] [![Coveralls]][Coveralls Link]

[Travis]: https://travis-ci.org/hiroaki-yamamoto/django-nghelp.svg?branch=master
[Travis Link]: https://travis-ci.org/hiroaki-yamamoto/django-nghelp
[Code Climate]: https://codeclimate.com/github/hiroaki-yamamoto/django-nghelp/badges/gpa.svg
[Code Climate Link]: https://codeclimate.com/github/hiroaki-yamamoto/django-nghelp
[Coveralls]: https://coveralls.io/repos/github/hiroaki-yamamoto/django-nghelp/badge.svg?branch=master
[Coveralls Link]: https://coveralls.io/github/hiroaki-yamamoto/django-nghelp?branch=master

# What This?
This repo contains code that help your AngularJS coding with Django.

# Why I invented?
When I started coding with Django and AngularJS, I needed to code the form to
embed model like this:

```Python
from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # They are already implemented because UserInfoForm inherit ModelForm
    # and the target model has the fields.
    widgets = {
      "age": forms.NumberInput(attrs={"data-ng-model": "model.age"}),
      "phone": forms.TextInput(attrs={"data-ng-model": "model.phone"}),
      "street": forms.TextInput(attrs={"data-ng-model": "model.street"}),
      "city": forms.TextInput(attrs={"data-ng-model": "model.city"}),
      "state": forms.TextInput(attrs={"data-ng-model": "model.state"})
    }
```

As you can see above, if you'd like to use AngularJS with django built-in
form, it needs to re-implement the fields that is already implemented. If
the forms to be implemented are few, it wouldn't be the problem, if you need
to implement many forms, you need to repeat above widget re-implementation
many times. This repo's code help to build AngularJS form like this:

```Python
from django import forms
from django_nghelp.forms import AngularForm

class UserInfoForm(AngularForm, forms.ModelForm):
  ng_model_prefix = "model" # Change this if you want to use other than "model"
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Automatically generates AngularJS forms.
```

# Features
This repo has 2 features of forms, and 4 widgets. For forms, they are
implemented for building AngularJS form, but the widgets are used for
[Angular Material].
[Angular Material]: https://github.com/angular/material

## Feature 1: Angular form
As you can see above sections, you'll need to implement redundant code:

```Python
from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # They are already implemented because UserInfoForm inherit ModelForm
    # and the target model has the fields.
    widgets = {
      "age": forms.NumberInput(attrs={"data-ng-model": "model.age"}),
      "phone": forms.TextInput(attrs={"data-ng-model": "model.phone"}),
      "street": forms.TextInput(attrs={"data-ng-model": "model.street"}),
      "city": forms.TextInput(attrs={"data-ng-model": "model.city"}),
      "state": forms.TextInput(attrs={"data-ng-model": "model.state"})
    }
```

However, you can implement simpler code by using `AngularForm`:

```Python
from django import forms
from django_nghelp.forms import AngularForm

class UserInfoForm(AngularForm, forms.ModelForm):
  ng_model_prefix = "model" # Change this if you want to use other than "model"
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Automatically generates AngularJS forms.
```

## Feature 2: All required forms
If you'd like to make all fields required on ModelForm, you will re-implement
entire fields like this:

```Python
from django import forms
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )

  # Assume that all fields are optional.
  age = forms.IntegerField(
    required=True,
    widget=forms.NumberInput(attrs={"data-ng-model": "model.age"})
  )
  phone = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.phone"})
  )
  street = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.street"})
  )
  city = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.city"})
  )
  state = forms.CharField(
    required=True,
    widget=forms.TextInput(attrs={"data-ng-model": "model.state"})
  )
```

Moreover, you will not be able to check if the field is proper unless you
refer Django's code. To reduce this time consumption, I implemented
`AllReqiuredForm`:

```Python
from django import forms
from django_nghelp.forms import AllRequiredForm
from .models import UserInfo

class UserInfoForm(AllRequiredForm, forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Assume that all fields are optional.
```

By using `AllRequiredForm`, you can reduce your LOC like above. Of course,
you can put optional field as exceptions like this:

```Python
from django import forms
from django_nghelp.forms import AllRequiredForm
from .models import UserInfo

class UserInfoForm(AllRequiredForm, forms.ModelForm):
  class Meta(object):
    model = UserInfo
    exclude = ("2fa_secret", )
    # Assume that all fields are optional.
    # By specifying optional, the specified fields won't
    # become a required field.
    optional = ("phone", )
```

## Features 3: Widgets for Angular Materials

If you like [Material Design], you'd also like to use [Angular Material], but
as you can see the doc. the components are using special tags. For example,
`select` and `option` input controllers should be replaced with `mdSelect` and
`mdOption` and they are not provided by built-in widgets.

This widget provides the widgets:

```Python
from django import forms
from django_nghelp.forms import AngularForm
from django_nghelp.widgets import (
  MDSelect, MDMultiSelect, MDDatePicker, MDDateSelect, MDCheckBox
)

from .models import ExampleModel

class ExampleForm(AngularForm, forms.ModelForm):
  class Meta(object):
    model = ExampleModel
    exclude = ("secret_field", )
    widgets = {
      "start_since": MDDateSelect(),
      "available_date": MDDatePicker(),
      "shape": MDSelect(choices=(
        ("F", "Fat"), ("N": "Normal"), ("T", "Thin")
      )),
      "needs_fill": MDCheckBox("Fill with border color?")
    }
```

[Material Design]: https://material.google.com/
[Angular Material]: https://material.angularjs.org

# Contribution
If you found bugs, feel free to send issues. However, sending a pull request
is more appreciated.
