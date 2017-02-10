angular.module('TheApples')

.controller("accountManager", function($scope, $rootScope, $http, $location, $window, $filter) {


  $scope.users = [];
  $scope.getUsers = function() {
    $http({
      method: 'GET',
      url: '/users/allUsers',
      headers: {
        'Content-Type': "application/json"
      }
    }).then(function successCallback(response) {
     console.log("success");
     console.log(response.data);
     $scope.users = response.data;
  }, function errorCallback(response) {
   console.log("error");
 });

  }
  $scope.getUsers();
  $scope.radioSelected = false;
  $scope.radioChanged = function(user) {
    $scope.current = {
      "id" : user.id,
      "first_name" : user.first_name,
      "last_name" : user.last_name,
      "username" : user.username,
      "role" : user.role,
      "password" : user.password
    }
    $scope.radioSelected = true;

  }
  $scope.openEdit = function() {
    $scope.edit = $scope.current;
  }


  $scope.new = {role: "faculty"};
  $scope.createUser = function() {
    $http({
      method: 'POST',
      url: '/users/createUser',
      headers: {
        'Content-Type': "application/json"
      },
      data: {
       'first_name': $scope.new.first_name,
       'last_name': $scope.new.last_name,
       'username': $scope.new.username,
       'password': $scope.new.password,
       'role': $scope.new.role
     }
   }).then(function successCallback(response) {
     $window.location.reload();
   }, function errorCallback(response) {
     console.log("error");
   });
 }

 $scope.editUser = function() {
  $http({
    method: 'POST',
    url: '/edit/user',
    headers: {
      'Content-Type': "application/json"
    },
    data: {
      'id': $scope.edit.id,
      'first_name': $scope.edit.first_name,
      'last_name': $scope.edit.last_name,
      'username': $scope.edit.username,
      'password': $scope.edit.password,
      'role': $scope.edit.role
    }
  }).then(function successCallback(response) {
    console.log("Calling edit user");
    $window.location.reload();
  }, function errorCallback(response) {
   console.log("error");
 });
}

$scope.deleteUser = function() {
  $http({
    method: 'POST',
    url: '/delete/user',
    headers: {
      'Content-Type': "application/json"
    },
    data: {
      'id': $scope.edit.id
    }
  }).then(function successCallback(response) {
    console.log("Calling delete user");
    $window.location.reload();
  }, function errorCallback(response) {
   console.log("error");
 });
}


$scope.backButtonClicked = function () {
  $location.path("/login");
}

})
