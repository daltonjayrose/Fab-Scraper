# Fab-Scraper
You can view the final result [here](http://loonafabarchive.com).

In 2022, the members of the South Korean girl group [LOONA](https://en.wikipedia.org/wiki/Loona) joined the messaging service [Fab](https://play.google.com/store/apps/details?id=com.neowizlab.fab&hl=en_US&gl=US) to communicate with their fans. While Fab had a feature to translate their messages from Korean to English, the translations were subpar as they utilized free or cheap translation services for the translations. Therefore, I wanted to develop a way to archive the messages LOONA posted to the service and provide better translations.

While Fab did not have a public API, I was able to examine HTTP requests sent/received from the app using an Android emulator to find a way to retrieve message data in JSON. Using Python, I wrote a simple program to retrieve the JSON and iterate through it, printing the messages to a markdown file. Markdown was chosen so that I could use the static site generator [MkDocs](https://www.mkdocs.org/) to generate a webpage to easily view the messages. I also utilized the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme so that messages could be easily searched. 

At this stage, the message text was still in Korean. I experimented with a few different translation libraries for Python with integration with Google Translate and the free version of Papago Translate. However, the translations provided by the free versions of these services was not very accurate. No public library existed for the premium version of Papago Translate but it was relatively simple to implement using their documentation. 

Note: When I worked on this project, I had no programming experience and had yet to learn about best practices for programming and my code reflects that.
