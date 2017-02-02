angular.module('TheApples')

.controller("facultyHome", function($scope, $rootScope, $location, $cookies) {
   $rootScope.bcrumb1 = null;
   $scope.name = "Timothy Kearns";
    $scope.logout = function() {
      console.log("logging out");
      $rootScope.role = null;
      $rootScope.user = null;
      $cookies.remove('user');
      $cookies.remove('role');
      $location.path("/login");
   }
})

.controller("preferences", function($scope, $rootScope) {
  $rootScope.bcrumb1 = "Preferences";

})

.controller("viewScheduleCalendar", function($scope, $rootScope) {
	$rootScope.bcrumb1 = "Published Schedules";
})

.controller("viewScheduleTable", function($scope, $rootScope) {
	 $rootScope.bcrumb1 = "Published Schedules";
})

.controller("viewYourSchedule", function($scope, $rootScope) {
	$rootScope.bcrumb1 = "Your Schedule";
})

