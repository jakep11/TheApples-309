angular.module('TheApples')

.controller("chairHome", function($scope, $rootScope, $location, $cookies) {
   $rootScope.bcrumb1 = null;
   $scope.name = "Timothy Kearns";
   $scope.numNotifications = 12;


   $scope.logout = function() {
      console.log("logging out");
      $rootScope.role = null;
      $rootScope.user = null;
      $cookies.remove('user');
      $cookies.remove('role');
      $location.path("/login");
   }
   
   
})

.controller("courseManager", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Course Manager";
})

.controller("facultyManager", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Faculty Manager";
   console.log("faculty manager page");

})

.controller("facultyPreferences", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Faculty Manager";
   $rootScope.bcrumb1Link = "#facultyManager";
   $rootScope.bcrumb2 = "Faculty Preferences";
})

.controller("generateSchedule", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Schedules";
   $rootScope.bcrumb1Link = "#schedules";
   $rootScope.bcrumb2 = "Current Schedule";
})

.controller("importData", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Import Data";
})

.controller("notifications", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Notifications";
})

.controller("roomManager", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Room Manager";

})

.controller("schedules", function($scope, $rootScope) {
      $rootScope.bcrumb1 = "Schedules";

})

.controller("viewSchedule", function($scope, $rootScope) {
   $rootScope.bcrumb1 = "Schedules";
   $rootScope.bcrumb1Link = "#schedules";
   $rootScope.bcrumb2 = "Current Schedule";
})

