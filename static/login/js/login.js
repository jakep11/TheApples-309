angular.module('TheApples').controller("login", function($scope, $rootScope, $location, $cookies) {
   
   $scope.continueAsGuest = function() {
      $rootScope.role = "student";
      $cookies.put('role', 'student');
      $location.path("/viewScheduleTableStudent");
   }
   $scope.login = function() {
      //Do stuff here
      if ($scope.username == "faculty" && $scope.password == "123") {
         $rootScope.role = "faculty";
         $cookies.put('role', 'faculty');
         $location.path("/facultyHome");
      }
      else if ($scope.username == "chair" && $scope.password == "123") {
         $rootScope.role = "chair";
         $cookies.put('role', 'chair');
         $location.path("/chairHome")
      }
      else if ($scope.username == "admin" && $scope.password == "123") {
         $rootScope.role = "admin";
         $cookies.put('role', 'admin');
         $location.path("/accountManager")
      }
      else {
         $scope.error = true;
      }
   }
})



