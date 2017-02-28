var app = angular.module('TheApples');

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

    this.previousSpan = [0, 0];
    this.previousDays = ["", ""];
});

app.controller("viewScheduleTableStudent", function ($scope, $rootScope, $location, $http, sharedData) {
    $rootScope.bcrumb1 = "Published Schedules";

    $scope.sortType = 'course_num';
    $scope.reverse = true;

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

        //
        // maybe move somewhere else; temporary position
        //
        $scope.showSelectedTerms();

        // arrays to hold selected filter values
        var terms = []
        var ids = [];
        var instructors = [];
        var timeStart = [];
        var timeEnd = [];

        // collect the selected term_ids and store in ids array
        angular.forEach($scope.checkedTerms, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, terms);
        // collect the selected course_ids and store in ids array
        angular.forEach($scope.checkedCourses, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, ids);
        // collect the selected faculty_ids and store in instructors array
        angular.forEach($scope.checkedInstructors, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, instructors);
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

        if (terms.length === 0) {
            terms.push($scope.terms[sharedData.lastTermIndex].id);
        }

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
            $scope.checkedTerms[sharedData.lastTermId] = true;

            // add the default selected term to be displayed
            $scope.showSelectedTerms();

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
            console.log(obj);
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

    // dynamically display term title and term's sections when checked and filters applied
    $scope.showSelectedTerms = function () {
        var showTerms = [];

        // check if a term is checked and should be displayed
        angular.forEach($scope.terms, function (term) {
            var termId = term.id;

            angular.forEach($scope.checkedTerms, function (value, key) {
                if (key === termId && value === true) {
                    this.push(term);
                }
            }, showTerms);
        });

        // if no terms are selected, display sections for the current (default) term
        if (showTerms.length === 0) {
            showTerms.push($scope.terms[sharedData.lastTermIndex]);
        }

        $scope.showTerms = showTerms;
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

    //
    // change this to get all sections for ONLY the current term
    //
    $scope.getSections = function () {
        $http({
            method: 'GET',
            url: '/get/allSections',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.sections = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getSections();

    // post feedback to the Comments table when Post Feedback is clicked
    $scope.postFeedback = function () {
       console.log("Posting feedback!");
       $http({
          method: 'POST',
          url: '/create/comment',
          headers: {
                'Content-Type': 'application/json'
          },
          data: {
                'term_id': $scope.term_id,
                'username': $scope.username,
                'comment': $scope.comment,
                'time': new Date().toLocaleString(),
                'unread': "true",
                'type': "Feedback"
          }
        }).then(function successCallback(response) {
            $scope.courses = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }

    // return to login page when back button is clicked
    $scope.backButtonClicked = function () {
        $location.path("/login");
    }
});

app.controller("viewScheduleCalendarStudent", function ($scope, $rootScope, $location, $http, sharedData) {
    $rootScope.bcrumb1 = "Published Schedules";

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

        // collect the selected term_ids and store in ids array
        angular.forEach($scope.checkedTerms, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, terms);
        // collect the selected course_ids and store in ids array
        angular.forEach($scope.checkedCourses, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, ids);
        // collect the selected faculty_ids and store in instructors array
        angular.forEach($scope.checkedInstructors, function (value, key) {
            if (value === true) {
                this.push(key);
            }
        }, instructors);
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

        if (terms.length === 0) {
            terms.push($scope.terms[sharedData.lastTermIndex].id);
        }

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

    $scope.getCourses = function () {
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
            $scope.checkedTerms = sharedData.lastTermId;

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
            console.log(obj);
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

    $scope.backButtonClicked = function () {
        $location.path("/login");
    }
    $scope.today = function () {
        $scope.dt = new Date();
    };
    $scope.today();

    $scope.clear = function () {
        $scope.dt = null;
    };

    $scope.inlineOptions = {
        customClass: getDayClass,
        minDate: new Date(),
        showWeeks: true
    };

    $scope.dateOptions = {
        dateDisabled: disabled,
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
    };

    // post feedback to the Comments table when Post Feedback is clicked
    $scope.postFeedback = function () {
       console.log("Posting feedback!");
       $http({
          method: 'POST',
          url: '/create/comment',
          headers: {
                'Content-Type': 'application/json'
          },
          data: {
                'term_id': $scope.term_id,
                'username': $scope.username,
                'comment': $scope.comment,
                'time': new Date().toLocaleString()
          }
        }).then(function successCallback(response) {
            $scope.courses = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }

    // Disable weekend selection
    function disabled(data) {
        var date = data.date,
            mode = data.mode;
        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
    }

    $scope.toggleMin = function () {
        $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
        $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
    };

    $scope.toggleMin();

    $scope.open1 = function () {
        $scope.popup1.opened = true;
    };

    $scope.setDate = function (year, month, day) {
        $scope.dt = new Date(year, month, day);
    };

    $scope.formats = ['shortDate'];
    $scope.format = $scope.formats[0];

    $scope.popup1 = {
        opened: false
    };

    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    var afterTomorrow = new Date();
    afterTomorrow.setDate(tomorrow.getDate() + 1);
    $scope.events = [
        {
            date: tomorrow,
            status: 'full'
    },
        {
            date: afterTomorrow,
            status: 'partially'
    }
  ];

    function getDayClass(data) {
        var date = data.date,
            mode = data.mode;
        if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0, 0, 0, 0);

            for (var i = 0; i < $scope.events.length; i++) {
                var currentDay = new Date($scope.events[i].date).setHours(0, 0, 0, 0);

                if (dayToCheck === currentDay) {
                    return $scope.events[i].status;
                }
            }
        }

        return '';
    }
});
