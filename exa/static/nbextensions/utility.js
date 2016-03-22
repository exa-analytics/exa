/*"""
===============
utility.js
===============
Helper functions used by custom notebook JS.
*/
'use strict';

/*require.config({
    shim: {
    },
});*/

define([], function() {
    var unique = function(obj) {
        /*"""
        unique
        ---------
        Get the unique values from an object.

        This is a call to the object's filter method passing the **_unique**
        function as the criteria.

        .. code-block:: javascript

            var a = ['a', 1, 'a', 2, '1'];
            var u = utility.unique(a);
            console.log(u);               // ["a", 1, 2, "1"]

        Args:
            obj (object): Array like object.

        See Also:
            **_unique**
        */
        return obj.filter(_unique);
    };

    var _unique = function(value, index, self) {
        /*"""
        _unique
        -----------
        Check if the given value is the first occurring and keep it if it is.
        */
        return self.indexOf(value) === index;
    };

    return {'unique': unique};
});
