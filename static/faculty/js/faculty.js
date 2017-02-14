var app = angular.module('TheApples')

app.controller("facultyHome", function ($scope, $rootScope, $location, $cookies) {
    $rootScope.bcrumb1 = null;

    $scope.logout = function () {
        console.log("logging out");
        $location.path("/login");
    }
})

app.controller("preferences", function ($scope, $rootScope, $http) {
    $rootScope.bcrumb1 = "Preferences";
    $scope.day = "Monday";

    $scope.getCourses = function () {
        console.log("getting courses");
        $http({
            method: 'GET',
            url: '/get/allCourses',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function successCallback(response) {
            $scope.courses = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getCourses();

    $scope.plusButtonClicked = function () {
        console.log("Filtering Courses");
        $http({
            method: 'POST',
            url: '/get/filterCourses',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'number': $scope.number
            }
        }).then(function successCallback(response) {
            $scope.courses = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.dayChanged = function () {
        console.log("Changing Day");
        $scope.day = $scope.dayChoice;
        console.log($scope.day);
        $scope.getCourses();
    }
    $scope.saveChanges = function () {
        console.log("Saving Changes");

    }

})

app.controller("viewScheduleCalendar", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Published Schedules";
})

app.controller("viewScheduleTable", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Published Schedules";
})

app.controller("viewYourSchedule", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Your Schedule"

    $(document).ready(function () {
        $('[data-toggle="popover"]').popover({
            placement: 'bottom',
            content: 'CPE 101-01 / Lecture / Room 14-256 CPE 103-03 / Lecture / Room 14-301'
        });
    });

})
