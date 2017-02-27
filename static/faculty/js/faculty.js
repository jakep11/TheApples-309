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

    var faculty = null;
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

app.controller("viewYourSchedule", function ($scope, $rootScope, $location, $http, sharedData) {
    // arrays to hold sections by day
    $scope.MWFsections = [];
    $scope.TRsections = [];

    $rootScope.bcrumb1 = "Your Schedule";

    $scope.startTimes = sharedData.startTimes;


    $scope.sortBy = function (sortType) {
        $scope.reverse = ($scope.sortType === sortType) ? !$scope.reverse : false;
        $scope.sortType = sortType;
    };


    // grab list of times from sharedData and populate UI
    $scope.startTimes = sharedData.startTimes;
    $scope.endTimes = sharedData.endTimes;

    // arrays to hold the values for checked checkboxes used for filtering sections
    $scope.checkedTerms = [];
    $scope.checkedCourses = [];
    $scope.checkedInstructors = [];
    $scope.checkedStartTimes = [];
    $scope.checkedEndTimes = [];

    $scope.applyFilters = function () {
        // testing checked checkbox values
        console.log($scope.terms);
        console.log($scope.checkedTerms);
        console.log($scope.checkedCourses);
        console.log($scope.checkedInstructors);
        console.log($scope.checkedStartTimes);
        console.log($scope.checkedEndTimes);

        // arrays to hold selected filter values
        var terms = []
        var ids = [];
        var instructors = [];
        var timeStart = [];
        var timeEnd = [];

        // collect the selected course_id and store in ids array
        terms.push($scope.checkedTerms.id);
        // collect the selected course_ids and store in ids array
        angular.forEach($scope.checkedCourses, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, ids);
        // collect the current faculty_id and store in instructors array
        instructors.push(sharedData.faculty.id);
        // collect the selected start time values and store in startTimes array
        angular.forEach($scope.checkedStartTimes, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, timeStart);
        // collect the selected end time values and store in endTimes array
        angular.forEach($scope.checkedEndTimes, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, timeEnd);

        // testing selected values arrays
        console.log(terms.length)
        console.log(ids.length);
        console.log(instructors.length);
        console.log(timeStart.length);
        console.log(timeEnd.length);

        // POST filter data to filters.py and retrieve filtered courses
        $http({
            method: 'POST',
            url: '/filter/sections',
            headers: {
                'Content-Type': "application/json"
            },
            data: {
                'terms': terms,
                'ids': ids,
                'instructors': instructors,
                'timeStart': timeStart,
                'timeEnd': timeEnd
            }
        }).then(function successCallback(response) {
            $scope.sections = response.data;
            console.log("success");
        }, function errorCallback(response) {
            console.log("error");
        });
    }

    console.log("work?"); // remove debugging for final version

    $scope.getCourses = function () {
        console.log("getting courses");
        $http({
            method: 'GET',
            url: '/get/allCourses',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.courses = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getCourses();

    $scope.getTerms = function () {
        $http({
            method: 'GET',
            url: '/get/terms',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.terms = response.data;

            // default select the current (newest/most recent) term
            $scope.findLastTermIndex();
            $scope.checkedTerms = $scope.terms[sharedData.lastTermIndex];

            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getTerms();

    $scope.findLastTermIndex = function () {
        var lastIndex;

        var year = -1;
        var quarterId = -1;

        angular.forEach($scope.terms, function (obj, index) {
            if (obj.year > year || (obj.year === year && obj.quarterId > quarterId)) {
                lastIndex = index;
                year = obj.year;
                quarterId = obj.quarterId;
            }
        });

        // add these values to shared data to use between functions/controllers
        sharedData.lastTermId = $scope.terms[lastIndex].id;
        sharedData.lastTermIndex = lastIndex;

        return lastIndex;
    }

    $scope.getInstructors = function () {
        $http({
            method: 'GET',
            url: '/get/instructors',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.instructors = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getInstructors();

    // get the faculty_id from the user that is currently logged in to display only their schedules
    $scope.getFacultyFromUser = function () {
        $http({
            method: 'POST',
            url: '/get/facultyFromUser',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
                'userID': $rootScope.user_id
            }
        }).then(function successCallback(response) {
            sharedData.faculty = response.data;
            $scope.applyFilters();
            console.log("success");
        }, function errorCallback(response) {
            console.log("error");
        });
    }
    $scope.getFacultyFromUser();

    //
    //    // return to login page when back button is clicked
    //    $scope.backButtonClicked = function () {
    //        $location.path("/login");
    //    }
});
