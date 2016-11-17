var widgets = require("jupyter-js-widgets");
var _ = require("underscore");
var base = require("./foo/base.js");


var ExampleModel = base.createWidgetModel("Example", {"value": "example text"});


class ExampleView extends widgets.DOMWidgetView {
    render() {
        this.value_changed();
        this.model.on("change:value", this.value_changed, this);
    }

    value_changed() {
        this.el.textContent = this.model.get("value");
    }
}


module.exports = {
    ExampleModel: ExampleModel,
    ExampleView: ExampleView
};
