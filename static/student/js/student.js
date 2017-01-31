angular.module('TheApples')

.controller("viewScheduleCalendarStudent", function($scope, $rootScope, $location) {
   $scope.backButtonClicked = function() {
      $location.path("/login");
   }
})

.controller("viewScheduleTableStudent", function($scope, $rootScope, $location) {
   $scope.backButtonClicked = function() {
      $location.path("/login");
   }
})

