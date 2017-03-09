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

    // retrieve all courses from the database
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

    // get the faculty_id from the user that is currently logged in to display their preferences
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
            console.log("success");
        }, function errorCallback(response) {
            console.log("error");
        });
    }
    $scope.getFacultyFromUser();
})

app.controller("viewScheduleCalendar", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Published Schedules";
})

app.controller("viewScheduleTable", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Published Schedules";
})

app.controller("viewYourSchedule", function ($scope, $rootScope, $location, $http, sharedData) {
    $rootScope.bcrumb1 = "Your Schedule";

    $scope.startTimes = sharedData.startTimes;

    // function to help with sorting
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

    // filter the course sections that will be displayed
    $scope.applyFilters = function () {
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

    // retrieve all courses from the database
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
            if (obj.published && obj.year > year || (obj.year === year && obj.quarterId > quarterId)) {
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

    // set the sections into the calendar view
    $scope.setCalendarCells = function (time) {
        var defaultVal = 5;
        var hours = [0, 0];
        var span;

        var sections = new Array(defaultVal);

        angular.forEach($scope.sections, function (obj) {
            if (obj.time_start === time) {
                if (obj.days == "MWF") {
                    this[0] = obj;
                    this[2] = obj;
                    this[4] = obj;

                    hours[0] += obj.hours;
                } else {
                    this[1] = obj;
                    this[3] = obj;

                    hours[1] += obj.hours;
                }
            }
        }, sections);

        if (sharedData.previousSpan[0] > 0 && sharedData.previousSpan[1] > 0) {
            sections = new Array();
            sharedData.previousSpan[0]--;
            sharedData.previousSpan[1]--;
        } else if (sharedData.previousSpan[0] > 0) {
            sections.splice(0, 1);
            sections.splice(1, 1);
            sections.splice(2, 1);

            sharedData.previousSpan[0]--;
        } else if (sharedData.previousSpan[1] > 0) {
            sections.splice(1, 1);
            sections.splice(2, 1);

            sharedData.previousSpan[1]--;
        }

        // keep track of how many rows the current MWF section spans
        if (sharedData.previousSpan[0] === 0) {
            sharedData.previousSpan[0] += Math.max((hours[0] * 2) - 1, 0);
        }
        // keep track of how many rows the current TR section spans
        if (sharedData.previousSpan[1] === 0) {
            sharedData.previousSpan[1] += Math.max((hours[1] * 2) - 1, 0);
        }

        return sections;
    }
});
