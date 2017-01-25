'use strict';   // See note about 'use strict'; below

console.log("hello");

var app = angular.module('TheApples', ['ngRoute']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/', 
    {
     templateUrl: 'static/partials/home.html',
    })
    .when('/about', 
    {
     templateUrl: 'static/partials/about.html',
    })
    .otherwise({
     redirectTo: '/'
    });
}]);