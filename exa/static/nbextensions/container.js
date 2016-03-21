/*"""
========================================
Container Module
========================================
An extension for the Jupyter notebook environment that allows for visualization
of exa's Container class.
*/
'use strict';


define(['widgets/js/widget'], function(widget) {
    var ContainerView = widget.DOMWidgetView.extend({
        /*"""
        ContainerView
        ===============
        Backbone.js view defined within the ipywidgets JavaScript environment.
        Below is a general outline of the structure of any "View" code.

        .. code-block:: javascript

            define(['widgets/js/widget'], function(widget) {
                var View = widget.DOMWidgetView.extend({
                    render: function() {
                        ...
                    },

                    other: function() {
                        ...
                    }
                });

                return {'View': View};
            });
        */
        init: function() {    // Overwritten when "subclassing" views
            //this.model.on('change:_____', this._____, this);
            var obj = this.get_trait('garbage');
            console.log(obj);
        },

        render: function() {
            /*"""
            render
            -------------
            Main entry point (akin to the constructor) for ipywidgets DOMWidget
            views.
            */
            console.log('container init');
            this.update_value();
            this.model.on('change:test_value', this.update_value, this);
            this.init();
            // Below is debug/test
            var obj1 = this.model.get('test_value');
            var obj2 = this.model.get('test_json');
            var obj3 = this.get_trait('test_value');
            var obj4 = this.get_trait('test_json');
            var obj5 = this.model.get('test_float');
            var obj6 = this.get_trait('test_float');
            console.log(typeof obj1);
            console.log(typeof obj2);
            console.log(typeof obj3);
            console.log(typeof obj4);
            console.log(typeof obj5);
            console.log(typeof obj6);
            console.log(obj1);
            console.log(obj2);
            console.log(obj3);
            console.log(obj4);
            console.log(obj5);
            console.log(obj6);
            console.log(obj2[0]);
            console.log(obj4[0]);
            console.log(obj5);
            console.log(obj6);
        },

        update_value: function() {
            /*"""
            update_value
            ----------------
            Updates the JS side value of the backend attribute "test_value".
            */
            this.value = this.get_trait('test_value');
            this.$el.text(this.value);
        },

        get_trait: function(name) {
            /*"""
            get_trait
            -------------
            Wrapper around the DOMWidgetView (Backbone.js) "model.get" function,
            that attempts to convert JSON strings to objects. Note that
            */
            var obj = this.model.get(name);
            if (typeof obj == 'string') {
                try {
                    obj = JSON.parse(obj);
                } catch(err) {
                    console.log(err);
                };
            };
            return obj;
        },
    });


    return {'ContainerView': ContainerView};
});
