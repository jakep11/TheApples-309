var app = angular.module('TheApples');

app.controller("viewScheduleTableStudent", function ($scope, $rootScope, $location, $http) {
    $scope.backButtonClicked = function () {
        $location.path("/login");
    }
    $scope.applyFilters = function () {
        $location.path("/view/allSections");
    }
    console.log("work?");
    $scope.getCourses = function() {
        console.log("getting courses");
      $http({
          method: 'GET',
          url: '/courses/allCourses',
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
    $scope.getTerms = function() {
      $http({
          method: 'GET',
          url: '/get/terms',
          headers: {
            'Content-Type': 'application/json'
          }
      }).then(function successCallback(response) {
        $scope.terms = response.data;
         console.log('success');
       }, function errorCallback(response) {
         console.log('error');
       });
    }
    $scope.getTerms();
});

app.controller("viewScheduleCalendarStudent", function ($scope, $rootScope, $location, $http) {

    $scope.getCourses = function() {
      $http({
          method: 'GET',
          url: '/courses/allCourses',
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
    $scope.getTerms = function() {
      $http({
          method: 'GET',
          url: '/get/terms',
          headers: {
            'Content-Type': 'application/json'
          }
      }).then(function successCallback(response) {
        $scope.terms = response.data;
         console.log('success');
       }, function errorCallback(response) {
         console.log('error');
       });
    }
    $scope.getTerms();
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
