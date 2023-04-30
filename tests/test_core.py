from dataclasses import dataclass

import pytest
from starlette.testclient import TestClient

from redmage import Component, Redmage, Target
from redmage.elements import Div, Element, Form, Input
from redmage.exceptions import RedmageError
from redmage.types import HTMXClass, HTMXSwap


def test_sanity():
    assert True


def test_redmage_create_app():
    app = Redmage()
    assert app.debug is False


def test_redmage_create_app_with_debug():
    app = Redmage(debug=True)
    assert app.debug is True


def test_component_constructor():
    class TestComponent(Component):
        def render(self):
            ...

    component = TestComponent()
    assert component.id


def test_redmage_register_component_with_no_targets():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return "Hello World"

    assert len(app.routes) == 0


def test_redmage_register_component_index():
    app = Redmage()

    class TestComponent(Component, routes=("/",)):
        def render(self):
            return Div("Hello World")

    assert len(app.routes) == 1
    assert app.routes[0].path == "/"

    client = TestClient(app.starlette)
    response = client.get("/")
    assert response.status_code == 200


def test_redmage_register_component_with_get_target_with_args():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.get
        def test_target(self, param1: int, param2: str):
            self.param1 = param1
            self.param2 = param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert (
        app.routes[0].path
        == "/TestComponent/{id:str}/test_target/{test_target__param1:int}/{test_target__param2:str}"
    )

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target/1/test")
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 test</div>'


def test_redmage_register_component_with_post_target_with_args():
    app = Redmage()

    @dataclass
    class TestSerializer:
        param1: int
        param2: str

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.post
        def test_target(self, test_serializer: TestSerializer, /):
            self.param1 = test_serializer.param1
            self.param2 = test_serializer.param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert app.routes[0].path == "/TestComponent/{id:str}/test_target"

    client = TestClient(app.starlette)
    response = client.post(
        "/TestComponent/1/test_target", data={"param1": 1, "param2": "test"}
    )
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 test</div>'


def test_redmage_register_component_with_put_target_with_args():
    app = Redmage()

    @dataclass
    class TestSerializer:
        param1: int
        param2: str

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.put
        def test_target(self, test_serializer: TestSerializer, /):
            self.param1 = test_serializer.param1
            self.param2 = test_serializer.param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert app.routes[0].path == "/TestComponent/{id:str}/test_target"

    client = TestClient(app.starlette)
    response = client.put(
        "/TestComponent/1/test_target", data={"param1": 1, "param2": "test"}
    )
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 test</div>'


def test_redmage_register_component_with_patch_target_with_args():
    app = Redmage()

    @dataclass
    class TestSerializer:
        param1: int
        param2: str

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.patch
        def test_target(self, test_serializer: TestSerializer, /):
            self.param1 = test_serializer.param1
            self.param2 = test_serializer.param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert app.routes[0].path == "/TestComponent/{id:str}/test_target"

    client = TestClient(app.starlette)
    response = client.patch(
        "/TestComponent/1/test_target", data={"param1": 1, "param2": "test"}
    )
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 test</div>'


def test_redmage_register_component_with_delete_target_with_args():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.delete
        def test_target(self, param1: int, param2: str):
            self.param1 = param1
            self.param2 = param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert (
        app.routes[0].path
        == "/TestComponent/{id:str}/test_target/{test_target__param1:int}/{test_target__param2:str}"
    )

    client = TestClient(app.starlette)
    response = client.delete("/TestComponent/1/test_target/1/test")
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 test</div>'


def test_redmage_register_component_with_get_target_with_query_params():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World {self.param1} {self.param2}")

        @Target.get
        def test_target(self, param1: int = 0, param2: str = "init"):
            self.param1 = param1
            self.param2 = param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert app.routes[0].path == "/TestComponent/{id:str}/test_target"

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target?test_target__param1=1")
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 1 init</div>'

    client = TestClient(app.starlette)
    response = client.get(
        "/TestComponent/1/test_target?test_target__param1=2&test_target__param2=test"
    )
    assert response.status_code == 200
    assert response.text.strip() == '<div id="TestComponent-1">Hello World 2 test</div>'


def test_redmage_register_component_with_annotations():
    app = Redmage()

    class TestComponent(Component):
        test_annotation: str

        def render(self):
            return Div(
                f"Hello World {self.test_annotation} {self.param1} {self.param2}"
            )

        @Target.get
        def test_target(self, param1: int = 0, param2: str = "init"):
            self.param1 = param1
            self.param2 = param2

    assert len(app.routes) == 1
    assert app.routes[0].name == "test_target"
    assert (
        app.routes[0].path
        == "/TestComponent/{id:str}/test_annotation/{test_annotation:str}/test_target"
    )

    client = TestClient(app.starlette)
    response = client.get(
        "/TestComponent/1/test_annotation/new_annotation/test_target?test_target__param1=1"
    )
    assert response.status_code == 200
    assert (
        response.text.strip()
        == '<div id="TestComponent-1">Hello World new_annotation 1 init</div>'
    )


def test_redmage_create_get_target():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(
                f"Hello World",
                target=self.test_target(1, param2="test"),
            )

        @Target.get
        def test_target(self, param1: int, param2: str = "init"):
            ...

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target/0/?test_target__param2=init")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == f'<div id="TestComponent-1" hx-swap="{HTMXSwap.OUTER_HTML}" hx-target="#TestComponent-1" hx-get="/TestComponent/1/test_target/1?test_target__param2=test">Hello World</div>'
    )


def test_redmage_create_get_target_with_annotation():
    app = Redmage()

    class TestComponent(Component):
        test_annotation: str

        def render(self):
            return Div(
                f"Hello World",
                target=self.test_target(1, param2="test"),
            )

        @Target.get
        def test_target(self, param1: int, param2: str = "init"):
            ...

    client = TestClient(app.starlette)
    response = client.get(
        "/TestComponent/1/test_annotation/test/test_target/0/?test_target__param2=init"
    )
    assert response.status_code == 200
    assert (
        response.text.strip()
        == f'<div id="TestComponent-1" hx-swap="{HTMXSwap.OUTER_HTML}" hx-target="#TestComponent-1" hx-get="/TestComponent/1/test_annotation/test/test_target/1?test_target__param2=test">Hello World</div>'
    )


def test_redmage_create_post_target():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(
                f"Hello World",
                target=self.test_target(self.param1),
            )

        @Target.post
        def test_target(self, test_id: int):
            self.param1 = test_id

    client = TestClient(app.starlette)
    response = client.post("/TestComponent/1/test_target/4")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == f'<div id="TestComponent-1" hx-swap="{HTMXSwap.OUTER_HTML}" hx-target="#TestComponent-1" hx-post="/TestComponent/1/test_target/4">Hello World</div>'
    )


def test_redmage_create_post_target_swap():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(
                f"Hello World",
                target=self.test_target(1, "bar"),
                swap=HTMXSwap.INNER_HTML,
            )

        @Target.post
        def test_target(self, test_id: int, test: str = "foo"):
            ...

    client = TestClient(app.starlette)
    response = client.post("/TestComponent/1/test_target/1")
    assert response.status_code == 200
    print(response.text)
    assert (
        response.text.strip()
        == f'<div id="TestComponent-1" hx-swap="{HTMXSwap.INNER_HTML}" hx-target="#TestComponent-1" hx-post="/TestComponent/1/test_target/1?test_target__test=bar">Hello World</div>'
    )


def test_redmage_create_post_target_indicator():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Div(
                f"Hello World",
                target=self.test_target(),
                indicator=True,
            )

        @Target.post
        def test_target(self):
            ...

    client = TestClient(app.starlette)
    response = client.post("/TestComponent/1/test_target")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == f'<div class="{HTMXClass.Indicator}" id="TestComponent-1" hx-swap="{HTMXSwap.OUTER_HTML}" hx-target="#TestComponent-1" hx-post="/TestComponent/1/test_target">Hello World</div>'
    )


def test_redmage_form():
    app = Redmage()

    @dataclass
    class TestSerializer:
        param1: int

    class TestComponent(Component):
        def render(self):
            return Form(
                Input(name="param1", value=1),
                target=self.test_target(),
            )

        @Target.post
        def test_target(self, test_serializer: TestSerializer, /):
            ...

    client = TestClient(app.starlette)
    response = client.post("/TestComponent/1/test_target", data={"param1": 1})
    assert response.status_code == 200
    assert (
        response.text.strip()
        == f'<form id="TestComponent-1" hx-swap="{HTMXSwap.OUTER_HTML}" hx-target="#TestComponent-1" hx-post="/TestComponent/1/test_target">\n<input name="param1" value="1"/></form>'
    )


def test_redmage_form_without_serializer():
    app = Redmage()

    class TestComponent(Component):
        def render(self):
            return Form(
                Input(name="param1", value=1),
                target=self.test_target(),
            )

        @Target.post
        def test_target(self):
            ...

    client = TestClient(app.starlette)
    with pytest.raises(RedmageError):
        client.post("/TestComponent/1/test_target", data={"param1": 1})


def test_redmage_component_that_returns_another_component():
    app = Redmage()

    class ChildComponent(Component):
        def render(self):
            return Div(f"Hello Child")

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World")

        @Target.get
        def test_target(self):
            child = ChildComponent()
            child._id = "ChildComponent-1"
            return child

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target")
    assert response.status_code == 200
    assert response.text.strip() == '<div id="ChildComponent-1">Hello Child</div>'


def test_redmage_component_that_returns_multiple_components():
    app = Redmage()

    class ChildComponent(Component):
        def render(self):
            return Div(f"Hello Child")

    class TestComponent(Component):
        def render(self):
            return Div(f"Hello World")

        @Target.get
        def test_target(self):
            child = ChildComponent()
            child._id = "ChildComponent-1"
            return child, child

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == '<div id="ChildComponent-1">Hello Child</div>\n\n<div id="ChildComponent-1">Hello Child</div>'
    )


def test_redamge_component_with_render_extenstion():
    app = Redmage()

    def extension(el):
        el.attrs(test="test")
        return el

    Component.add_render_extension(extension=extension)

    class TestComponent(Component):
        def render(self, extension=extension):
            return extension(Div(f"Hello World"))

        @Target.get
        def test_target(self):
            ...

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == '<div id="TestComponent-1" test="test">Hello World</div>'
    )


def test_redamge_component_with_render_extenstion_var_keyword():
    app = Redmage()

    def extension(el):
        el.attrs(test="test")
        return el

    Component.add_render_extension(extension=extension)

    class TestComponent(Component):
        def render(self, **exts):
            return exts["extension"](Div(f"Hello World"))

        @Target.get
        def test_target(self):
            ...

    client = TestClient(app.starlette)
    response = client.get("/TestComponent/1/test_target")
    assert response.status_code == 200
    assert (
        response.text.strip()
        == '<div id="TestComponent-1" test="test">Hello World</div>'
    )
