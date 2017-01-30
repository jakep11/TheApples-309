angular.module('TheApples').controller("login", function($scope, $rootScope, $location) {
   
   $scope.continueAsGuest = function() {
      $rootScope.role = "student";
      $location.path("/viewScheduleCalendar");
   }
   $scope.login = function() {
      //Do stuff here
      if ($scope.username == "faculty" && $scope.password == "123") {
         $rootScope.role = "faculty";
         $location.path("/facultyHome");
      }
      else if ($scope.username == "chair" && $scope.password == "123") {
         $rootScope.role = "chair";
         $location.path("/chairHome")
      }
      else {
         $scope.error = true;
      }
   }
})



