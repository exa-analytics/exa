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

        render: function() {
            /*"""
            render
            -------------
            Main entry point (akin to a constructor).
            */
            var self = this;
            this.value_changed();   // Update to current value
            // Listen to backend changes
            this.model.on('change:_value', this.value_changed, this);
        },

        value_changed: function() {
            /*"""
            value_changed
            -------------------
            Custom function.
            */
            var value = this.model.get('_value');
            console.log(value);
            this.$el.text(value);
        }
    });

    return {'ContainerView': ContainerView};
});
