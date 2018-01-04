var ipywidgets = require("@jupyter-widgets/base");
var three = require("three");


console.log(ipywidgets);
console.log(three);


class TestWidgetView extends ipywidgets.DOMWidgetView {
    render() {
        console.log("here");
        console.log(this.model.get("value"));
    }
}

class TestWidgetModel extends ipywidgets.DOMWidgetModel {
    defaults() {
        return Object.assign({}, super.defaults(), {
            '_view_name': "TestWidgetView",
            '_view_module': "exa",
            '_view_module_version': "^0.4.0",
            '_model_name': "TestWidgetModel",
            '_model_module': "exa",
            '_model_module_version': "^0.4.0",
            'value': "Hello World",
        });
    }
}

module.exports = {
    TestWidgetView: TestWidgetView,
    TestWidgetModel: TestWidgetModel
};
