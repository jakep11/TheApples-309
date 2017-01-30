//This file sets up AngularJS and determines the routing. 

'use strict';   // Enforces better JavaScript practices

var app = angular.module('TheApples', ['ngRoute', 'ui.bootstrap']);

//This is how Angular determines what page to display based on the URL.
//Note: The controller will be in the same parent folder as the templateUrl
// but in the js folder
app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    //This is the home page
    .when('/', {
     templateUrl: 'static/login/html/login.html',
     controller: 'login'
    })
    //This specifies the controller and template html page for the login page
    .when('/login', {
     templateUrl: 'static/login/html/login.html',
     controller: 'login'
    })
    .when('/facultyHome', {
     templateUrl: 'static/faculty/html/facultyHome.html',
     controller: "facultyHome"
    })
    //If none of the "when"s are matched then it defaults to the home page. 
    .otherwise({
     redirectTo: '/'
    });
}]);


