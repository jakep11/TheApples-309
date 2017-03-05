//This file sets up AngularJS and determines the routing. 

'use strict';   // Enforces better JavaScript practices

var app = angular.module('TheApples', ['ngRoute',  'ui.bootstrap', 'ngCookies']);

//Runs every time the page is reloaded. Sets the role and user from the browser cookies
app.run(function($rootScope, $cookies) {
  $rootScope.role = $cookies.get('role');
  $rootScope.user = $cookies.get('user');
  $rootScope.user_id = $cookies.get('user_id');
  //Resetting the breadcrumbs when view changes
  $rootScope.$on("$locationChangeStart", function(event, next, current) { 
        $rootScope.bcrumb1Link = null;
        $rootScope.bcrumb2 = null;
    });

})

//Models the href functionality of a link but for Angular routing.
//Use go-click="somewhere" in code to jump to a new view
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
    })
    //This specifies the controller and template html page for the login page
    .when('/login', {
       templateUrl: 'static/login/html/login.html',
       controller: 'login',
    })
    //Page for the admin to veiw
    .when('/accountManager', {
       templateUrl: 'static/admin/html/accountManager.html',
       controller: "accountManager",
    })
    //Every page for a student to view
    .when('/viewScheduleTableStudent', {
       templateUrl: 'static/student/html/viewScheduleTableStudent.html',
       controller: "viewScheduleTableStudent",
    })
    .when('/viewScheduleCalendarStudent', {
       templateUrl: 'static/student/html/viewScheduleCalendarStudent.html',
       controller: "viewScheduleCalendarStudent",
    })
    //Every page for a faculty to view
    .when('/facultyHome', {
       templateUrl: 'static/faculty/html/facultyHome.html',
       controller: "facultyHome",
    })
    .when('/preferences', {
       templateUrl: 'static/faculty/html/preferences.html',
       controller: "preferences",
    })
    .when('/viewYourSchedule', {
       templateUrl: 'static/faculty/html/viewYourSchedule.html',
       controller: "viewYourSchedule",
    })

    //Every page for a chair to view
    .when('/chairHome', {
       templateUrl: 'static/chair/html/chairHome.html',
       controller: "chairHome",
    })
    .when('/courseManager', {
       templateUrl: 'static/chair/html/courseManager.html',
       controller: "courseManager",
    })
    .when('/facultyManager', {
       templateUrl: 'static/chair/html/facultyManager.html',
       controller: "facultyManager",
    })
    .when('/facultyPreferences', {
       templateUrl: 'static/chair/html/facultyPreferences.html',
       controller: "facultyPreferences",
    })
    .when('/generateSchedule', {
       templateUrl: 'static/chair/html/generateSchedule.html',
       controller: "generateSchedule",
    })
    .when('/importData', {
       templateUrl: 'static/chair/html/importData.html',
       controller: "importData",
    })
    .when('/notifications', {
       templateUrl: 'static/chair/html/notifications.html',
       controller: "notifications",
    })
    .when('/roomManager', {
       templateUrl: 'static/chair/html/roomManager.html',
       controller: "roomManager",
    })
    .when('/schedules', {
       templateUrl: 'static/chair/html/schedules.html',
       controller: "schedules",
    })
    .when('/viewSchedule', {
       templateUrl: 'static/chair/html/viewSchedule.html',
       controller: "viewSchedule",
    })
    .when('/historicData', {
       templateUrl: 'static/chair/html/historicData.html',
       controller: "historicData",
    })
    
    //If none of the "when"s are matched then it defaults to the home page. 
    .otherwise({
       redirectTo: '/'
    });
 }]);
