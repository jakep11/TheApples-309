angular.module('TheApples')

.controller("accountManager", function($scope, $rootScope, $http, $location) {

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

	$scope.createUser = function() {
		$http({
          method: 'POST',
          url: '/users/createUser',
          headers: {
            'Content-Type': "application/json"
          },
          data: {
          	'first_name': $scope.firstName,
          	'last_name': $scope.lastName,
          	'username': $scope.username,
          	'password': $scope.password,
          	'role': $scope.role
          }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response);
       }, function errorCallback(response) {
         console.log("error");
       });

	}
   
})