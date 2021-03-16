# Tutorial 5

## A. Code Review

1. Your tutor will break up into groups for this activity. Take a look at [this webpage](https://www.youtube.com/watch?v=GfL5zOhpB14). What routes do you think are necessary to allow this webpage to function? For each route:
 * Discuss the data it might take in
 * Discuss the data it might return

Your tutor may provide you with a [hackmd.io](https://hackmd.io) file for everyone to edit together.

2. Are there any considerations that need to be made when choosing how to breakup routes?

## B. Writing a route

1. Write a simple flask server [names.py](names.py) that does the following:
 * Has a route that can take a name and a date of birth (as a [unix timestamp](https://www.epochconverter.com/))
 * Has a route that will produce all names/ages of people who've been entered previously

*Ensure pylint is run on your code.*

## C. Testing a server

Write a flask server [key.py](key.py) that has a single route `/getcount?tag=img` where it loads the unsw homepage and counts how many times the HTML tag "tag" property appears in the page.
```html
<div id="a"></div>
```

counts as 1 div tag.

```json
{
    "tag_count": 125
}
```

Write a series of HTTP level system tests [key_test.py](key_test.py) to ensure it's behaving as expected. See week 4 lecture slides for inspiration.

*Ensure pylint is run on your code.*

## D. Auth V Auth

What are some real world examples of authentication and authorisation?

## E. Network questions

1. What is the difference between the internet and the world wide web? What network protocols are used in each?

2. Breakdown the key components of an HTTP URL, such as http://unsw.com/calendar/view?term=t3&week=5#top

## F. JSON & YAML

* Convert the JSON file [data_1.json](data_1.json) to YAML in [data_1.yml](data_1.yml)
* Convert the YAML file [data_2.yml](data_2.yml) to JSON in [data_2.json](data_2.json)

Of course, you can do this with [simple online tools](https://www.json2yaml.com/). However, we encourage you to try and do this manually because during the exam if we test you on these items you need to be prepared!
