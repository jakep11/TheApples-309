angular.module('TheApples').controller("login", function($scope, $rootScope, $http, $location, $cookies) {

   $scope.continueAsGuest = function() {
      $rootScope.role = "student";
      $cookies.put('role', 'student');
      //$location.path("/viewScheduleTableStudent");

      $http({
          method: 'POST',
          url: '/users/createUser',
          headers: {
            'Content-Type': "application/json"
          },
          data: {
            'first_name': 'from',
            'last_name': 'angular',
            'username': 'uname',
            'password': 'pleasehashme',
            'role': 'adminaaa'
          }
      }).then(function successCallback(response) {
         console.log("success");
       }, function errorCallback(response) {
         console.log("error");
       });

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



