//This file sets up AngularJS and determines the routing. 

'use strict';   // Enforces better JavaScript practices

var app = angular.module('TheApples', ['ngRoute',  'ui.bootstrap']);



//This is how Angular determines what page to display based on the URL.
//Note: The controller will be in the same parent folder as the templateUrl but in the js folder
//"css" value is optional 
app.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    //This is the home page
    .when('/', {
       templateUrl: 'static/login/html/login.html',
       controller: 'login',
       css: 'static/login/css/login.css'
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
    .when('/viewScheduleCalendar', {
       templateUrl: 'static/student/html/viewScheduleCalendar.html',
       controller: "viewScheduleCalendar"
    })
    .when('/chairHome', {
       templateUrl: 'static/chair/html/chairHome.html',
       controller: "chairHome"
    })
    
    //If none of the "when"s are matched then it defaults to the home page. 
    .otherwise({
       redirectTo: '/'
    });
 }]);


//This allows for partial css files to accompany each view. Don't try to understand
app.directive('head', ['$rootScope','$compile',
  function($rootScope, $compile){
    return {
      restrict: 'E',
      link: function(scope, elem){
        var html = '<link rel="stylesheet" ng-repeat="(routeCtrl, cssUrl) in routeStyles" ng-href="{{cssUrl}}" />';
        elem.append($compile(html)(scope));
        scope.routeStyles = {};
        $rootScope.$on('$routeChangeStart', function (e, next, current) {
          if(current && current.$$route && current.$$route.css){
            if(!angular.isArray(current.$$route.css)){
              current.$$route.css = [current.$$route.css];
           }
           angular.forEach(current.$$route.css, function(sheet){
              delete scope.routeStyles[sheet];
           });
        }
        if(next && next.$$route && next.$$route.css){
         if(!angular.isArray(next.$$route.css)){
           next.$$route.css = [next.$$route.css];
        }
        angular.forEach(next.$$route.css, function(sheet){
           scope.routeStyles[sheet] = sheet;
        });
     }
  });
     }
  };
}
]);

