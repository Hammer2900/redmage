from redmage import Component, Redmage
from redmage.elements import H1, Body, Doc, Head, Html, Script, Title

app = Redmage()


class Index(Component, routes=("/",)):
    def render(self):
        return Doc(
            Html(
                Head(
                    Title("Redmage | Example 1"),
                ),
                Body(
                    H1("Hello Redmage"),
                    Script(src="https://unpkg.com/htmx.org@1.8.5"),
                ),
            )
        )
