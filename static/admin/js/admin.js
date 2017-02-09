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
         if ($scope.users) $scope.current = $scope.users[0];
       }, function errorCallback(response) {
         console.log("error");
       });

    }
    $scope.getUsers();

  $scope.radioSelected = function(user) {
    $scope.edit = user;
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
          	'first_name': $scope.new.firstName,
          	'last_name': $scope.new.lastName,
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

    $scope.backButtonClicked = function () {
        $location.path("/login");
    }

})
