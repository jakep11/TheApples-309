var app = angular.module('TheApples')

// service will be used to help transfer between table and calendar view
app.service("sharedData", function () {
    // lists of time integer values and their corresponding 12 hour time
    this.startTimes = {
        700: "7:00AM",
        730: "7:30AM",
        800: "8:00AM",
        830: "8:30AM",
        900: "9:00AM",
        930: "9:30AM",
        1000: "10:00AM",
        1030: "10:30AM",
        1100: "11:00AM",
        1130: "11:30AM",
        1200: "12:00PM",
        1230: "12:30PM",
        1300: "1:00PM",
        1330: "1:30PM",
        1400: "2:00PM",
        1430: "2:30PM",
        1500: "3:00PM",
        1530: "3:30PM",
        1600: "4:00PM",
        1630: "4:30PM",
        1700: "5:00PM",
        1730: "5:30PM",
        1800: "6:00PM",
        1830: "6:30PM",
        1900: "7:00PM",
        1930: "7:30PM",
        2000: "8:00PM",
        2030: "8:30PM",
        2100: "9:00PM",
        2130: "9:30PM",
        2200: "10:00PM"
    };

    this.endTimes = {
        800: "8:00AM",
        830: "8:30AM",
        900: "9:00AM",
        930: "9:30AM",
        1000: "10:00AM",
        1030: "10:30AM",
        1100: "11:00AM",
        1130: "11:30AM",
        1200: "12:00PM",
        1230: "12:30PM",
        1300: "1:00PM",
        1330: "1:30PM",
        1400: "2:00PM",
        1430: "2:30PM",
        1500: "3:00PM",
        1530: "3:30PM",
        1600: "4:00PM",
        1630: "4:30PM",
        1700: "5:00PM",
        1730: "5:30PM",
        1800: "6:00PM",
        1830: "6:30PM",
        1900: "7:00PM",
        1930: "7:30PM",
        2000: "8:00PM",
        2030: "8:30PM",
        2100: "9:00PM",
        2130: "9:30PM",
        2200: "10:00PM"
    };

    var lastTermIndex = null;
    var lastTermId = null;
});

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

app.controller("viewYourSchedule", function ($scope, $rootScope, sharedData) {
    $rootScope.bcrumb1 = "Your Schedule"

    $scope.startTimes = sharedData.startTimes;


})
