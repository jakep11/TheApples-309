angular.module('TheApples').controller("login", function($scope, $rootScope, $http, $location, $cookies) {

  //Reset all rootScope variables when you go back to login page
  $rootScope.role = null;
  $rootScope.username = null;
  $rootScope.first_name = null;
  $rootScope.last_name = null;
  $cookies.remove('user');
  $cookies.remove('role');

   $scope.continueAsGuest = function() {
      $rootScope.role = "student";
      $cookies.put('role', 'student');
      $location.path("/viewScheduleTableStudent");

      
 }

$scope.createUser = function() {
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
            'role': 'admin'
          }
      }).then(function successCallback(response) {
         console.log("success");
       }, function errorCallback(response) {
         console.log("error");
       });

}

 $scope.login = function() {

  //Leave this validation in until the database is stable
  if ($scope.username == "faculty" && $scope.password == "123") {
         $rootScope.role = "faculty";
         $cookies.put('role', 'faculty');
         $location.path("/facultyHome");
      }
      else if ($scope.username == "chair" && $scope.password == "123") {
         $rootScope.role = "chair";
         $cookies.put('role', 'chair');
         $location.path("/chairHome");
      }
      else if ($scope.username == "admin" && $scope.password == "123") {
         $rootScope.role = "admin";
         $cookies.put('role', 'admin');
         $location.path("/accountManager");
      }
      else {
         
      

      
      $http({
          method: 'POST',
          url: '/users/validateLogin',
          headers: {
            'Content-Type': "application/json"
          },
          data: {
            'username': $scope.username,
            'password': $scope.password,
          }
      }).then(function successCallback(response) {
         var data = response.data;
         if (!data.isUser) {
            $scope.error = true;
         }
         else {
            if (data.role == "faculty") {
               $rootScope.role = "faculty";
               $location.path("/facultyHome");
            }
            else if (data.role == "chair") {
               $rootScope.role = "chair";
               $location.path("/chairHome")
            }
            else if (data.role == "admin") {
               $rootScope.role = "admin";
               $location.path("/accountManager")
            }
            else {
               $rootScope.role = "student"; //Putting role as student for now if it doesn't match anything
               $location.path("/viewScheduleTableStudent")
            }
            $rootScope.user = data.first_name + " " + data.last_name;
            $rootScope.user_id = data.id;
            $cookies.put('role', $rootScope.role);
            $cookies.put('user', $rootScope.user);
            $cookies.put('user_id', $rootScope.user_id);



         }
       }, function errorCallback(response) {
         console.log("error valdating login");
       });

      }
      
   }
})



