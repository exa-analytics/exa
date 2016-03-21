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
        init: function() {},    // Overwritten when "subclassing" views

        render: function() {
            /*"""
            render
            -------------
            Main entry point (akin to the constructor) for ipywidgets DOMWidget
            views.
            */
            console.log('container');
            this.update_trait_names();
            this.model.on('change:_trait_names', this.update_trait_names, this);
            this.init();
        },

        update_trait_names: function() {
            this._trait_names = this.model.get('_trait_names');
            console.log(this._trait_names);
        },

/*        set_listeners: function() {
            this._names = this.model.get('_trait_names');
            for (let name of this._names) {
                this[name] = this.model.get(name);
                this.update_trait(name);
                this.model.on('change:'.concat(name), this.update_trait, this);
            };
        },

        update_trait: function(name) {
            console.log('update_trait');
            console.log(name);
        },

        value_changed: function() {
            var value = this.model.get('_value');
            console.log(value);
            this.$el.text(value);
        }*/
    });

    return {'ContainerView': ContainerView};
});
