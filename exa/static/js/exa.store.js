'use strict';

class Store {
    constructor() {};

    render() {
        var self = this;
        console.log('Hello World');
        console.log(self);
    };
};


var store = new Store();


$(document).ready(function(){
    //var store = new Store();

    $("#b_click").click(function() {
        store.render();
    });
});
