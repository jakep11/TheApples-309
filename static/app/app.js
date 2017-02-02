//This file sets up AngularJS and determines the routing. 

'use strict';   // Enforces better JavaScript practices

var app = angular.module('TheApples', ['ngRoute',  'ui.bootstrap', 'ngCookies']);

//Runs every time the page is reloaded. Sets the role and user from the browser cookies
app.run(function($rootScope, $cookies) {
  $rootScope.role = $cookies.get('role');
  $rootScope.user = $cookies.get('user');
  //Resetting the breadcrumbs when view changes
  $rootScope.$on("$locationChangeStart", function(event, next, current) { 
        $rootScope.bcrumb1Link = null;
        $rootScope.bcrumb2 = null;
    });

})

app.directive( 'goClick', function ( $location ) {
  return function ( scope, element, attrs ) {
    var path;

    attrs.$observe( 'goClick', function (val) {
      path = val;
    });

    element.bind( 'click', function () {
      scope.$apply( function () {
        $location.path( path );
      });
    });
  };
});

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
       controller: 'login',
       css: 'static/login/css/login.css'
    })
    //Page for the admin to veiw
    .when('/accountManager', {
       templateUrl: 'static/admin/html/accountManager.html',
       controller: "accountManager",
       css: "static/admin/css/admin.css"
    })
    //Every page for a student to view
    .when('/viewScheduleCalendarStudent', {
       templateUrl: 'static/student/html/viewScheduleCalendarStudent.html',
       controller: "viewScheduleCalendarStudent",
       css: "static/student/css/student.css"
    })
    .when('/viewScheduleTableStudent', {
       templateUrl: 'static/student/html/viewScheduleTableStudent.html',
       controller: "viewScheduleTableStudent",
       css: "static/student/css/table.css"
    })

    //Every page for a faculty to view
    .when('/facultyHome', {
       templateUrl: 'static/faculty/html/facultyHome.html',
       controller: "facultyHome",
       css: "static/faculty/css/faculty.css"
    })
    .when('/preferences', {
       templateUrl: 'static/faculty/html/preferences.html',
       controller: "preferences",
       css: "static/faculty/css/faculty.css"
    })
    .when('/viewScheduleCalendar', {
       templateUrl: 'static/faculty/html/viewScheduleCalendar.html',
       controller: "viewScheduleCalendar",
       css: "static/faculty/css/faculty.css"
    })
    .when('/viewScheduleTable', {
       templateUrl: 'static/faculty/html/viewScheduleTable.html',
       controller: "viewScheduleTable",
       css: "static/faculty/css/faculty.css"
    })
    .when('/viewYourSchedule', {
       templateUrl: 'static/faculty/html/viewYourSchedule.html',
       controller: "viewYourSchedule",
       css: "static/faculty/css/faculty.css"
    })

    //Every page for a chair to view
    .when('/chairHome', {
       templateUrl: 'static/chair/html/chairHome.html',
       controller: "chairHome",
       css: "static/chair/css/chair.css"
    })
    .when('/courseManager', {
       templateUrl: 'static/chair/html/courseManager.html',
       controller: "courseManager",
       css: "static/chair/css/chair.css"
    })
    .when('/facultyManager', {
       templateUrl: 'static/chair/html/facultyManager.html',
       controller: "facultyManager",
       css: "static/chair/css/chair.css"
    })
    .when('/facultyPreferences', {
       templateUrl: 'static/chair/html/facultyPreferences.html',
       controller: "facultyPreferences",
       css: "static/chair/css/chair.css"
    })
    .when('/generateSchedule', {
       templateUrl: 'static/chair/html/generateSchedule.html',
       controller: "generateSchedule",
       css: "static/chair/css/chair.css"
    })
    .when('/importData', {
       templateUrl: 'static/chair/html/importData.html',
       controller: "importData",
       css: "static/chair/css/chair.css"
    })
    .when('/notifications', {
       templateUrl: 'static/chair/html/notifications.html',
       controller: "notifications",
       css: "static/chair/css/chair.css"
    })
    .when('/roomManager', {
       templateUrl: 'static/chair/html/roomManager.html',
       controller: "roomManager",
       css: "static/chair/css/chair.css"
    })
    .when('/schedules', {
       templateUrl: 'static/chair/html/schedules.html',
       controller: "schedules",
       css: "static/chair/css/chair.css"
    })
    .when('/viewSchedule', {
       templateUrl: 'static/chair/html/viewSchedule.html',
       controller: "viewSchedule",
       css: "static/chair/css/chair.css"
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

    Contact GitHub API Training Shop Blog About 

    © 2017 GitHub, Inc. Terms Privacy Security Status Help 

