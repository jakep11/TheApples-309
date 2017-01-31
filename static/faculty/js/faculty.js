angular.module('TheApples')

.controller("facultyHome", function($scope, $rootScope, $location, $cookies) {
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

.controller("preferences", function($scope) {

})

.controller("viewScheduleCalendar", function($scope) {
	
})

.controller("viewScheduleTable", function($scope) {
	
})

.controller("viewYourSchedule", function($scope) {
	
})

