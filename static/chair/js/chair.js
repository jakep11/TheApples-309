angular.module('TheApples')

.controller("chairHome", function($scope, $rootScope, $location, $cookies) {
   
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

.controller("courseManager", function($scope) {

})

.controller("facultyManager", function($scope) {
   
})

.controller("facultyPreferences", function($scope) {
   
})

.controller("generateSchedule", function($scope) {
   
})

.controller("importData", function($scope) {
   
})

.controller("notifications", function($scope) {
   
})

.controller("roomManager", function($scope) {
   
})

.controller("schedules", function($scope) {
   
})

.controller("viewSchedule", function($scope) {
   
})

