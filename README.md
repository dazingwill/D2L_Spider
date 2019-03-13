# D2L Spider

## Overview

A spider based on Scrapy to crawl the course discussions data in [USC DEN D2L](https://courses.uscden.net).

## Prerequisites

* Must have an USC account and the access to the discussions.

* Chrome or Firefox, cookies available.

* Python 3

* Install Scrapy

  ```
  pip install scrapy
  ```

* Install browser_cookie3

  ```
  pip install browser_cookie3
  ```

## Usage

### Login in browser

The spider will directly use cookies in your browser to access D2L. So make sure you have log in D2L and the cookies has not expire.

Just go https://courses.uscden.net and see if you are redirected to your student page.

### Config

Change the file *D2L_Spider/d2l_settings.example.py* to *D2L_Spider/d2l_settings.py* .

Set the URL of the discussion page you want to crawl

```
D2L_DISCUSSION_URL = "https://courses.uscden.net/d2l/le/{discussion id}/discussions/List"
```

If necessary, set exporter class to get output files in another format

```
D2L_EEXPORTER_CLASS = CsvItemExporter
```

You can find more general settings in *D2L_Spider/settings.py* .

### Run

In the project root:

```
scrapy crawl topic
```

### Result

The spider will crawl the whole discussion.

After finish, there will be 4 output files in the project root.

Corresponding to 4 level contents: Forum, Topic, Thread and Post.

Their fields are defined in *D2L_Spider/items.py* .

## Refers

[USC DEN](https://courses.uscden.net)

[Scrapy Document](https://scrapy.org/doc/)

[browser_cookie3](https://github.com/borisbabic/browser_cookie3)