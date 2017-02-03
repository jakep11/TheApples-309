angular.module('TheApples')

.controller("facultyHome", function($scope, $rootScope, $location, $cookies) {
   $rootScope.bcrumb1 = null;
   
    $scope.logout = function() {
      console.log("logging out");
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

