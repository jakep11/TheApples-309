angular.module('TheApples').controller("chairHome", function($scope, $rootScope, $location) {
   
   $scope.name = "Timothy Kearns";
   $scope.numNotifications = 12;

   $scope.goToPreferences = function() {
      $rootScope.role = "chair";
      $location.path("/facultyPreferences");
   }
   
})
