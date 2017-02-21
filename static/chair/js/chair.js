var app = angular.module('TheApples')


app.controller('chairHome', function ($scope, $rootScope, $location, $cookies) {
   $rootScope.bcrumb1 = null;

   $scope.numNotifications = 12;

   $scope.logout = function () {
      console.log('logging out');
      $location.path('/login');
   }


})

app.controller('courseManager', function ($scope, $rootScope, $http, $window) {
   $rootScope.bcrumb1 = 'Course Manager';

   $scope.getCourses = function () {
      $http({
         method: 'GET',
         url: 'get/allCourses',
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
   $scope.radioSelected = false;

   $scope.radioChanged = function (course) {
      $scope.current = {
         'id': course.id,
         'number': course.number,
         'major': course.major,
         'lecture_workload_units': course.lecture_workload_units,
         'lecture_hours': course.lecture_hours,
         'lab_workload_units': course.lab_workload_units,
         'lab_hours': course.lab_hours
      }
      $scope.radioSelected = true;

   }
   $scope.openEdit = function () {
      $scope.edit = $scope.current;
   }

   $scope.addCourse = function () {
      $http({
         method: 'POST',
         url: '/create/course',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'major': $scope.new.major,
            'number': $scope.new.number,
            'lecture_workload_units': $scope.new.lecture_workload_units,
            'lecture_hours': $scope.new.lecture_hours,
            'lab_workload_units': $scope.new.lab_workload_units,
            'lab_hours': $scope.new.lab_hours
         }
      }).then(function successCallback(response) {
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.editCourse = function () {
      $http({
         method: 'POST',
         url: '/edit/user',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'id': $scope.edit.id,
            'major': $scope.edit.major,
            'number': $scope.edit.number,
            'lecture_workload_units': $scope.edit.lecture_workload_units,
            'lecture_hours': $scope.edit.lecture_hours,
            'lab_workload_units': $scope.edit.lab_workload_units,
            'lab_hours': $scope.edit.lab_hours
         }
      }).then(function successCallback(response) {
         console.log('Calling edit course');
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.deleteCourse = function () {
      console.log("trying to delete course");
      $http({
         method: 'POST',
         url: '/delete/course',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'id': $scope.current.id
         }
      }).then(function successCallback(response) {
         console.log('Calling delete course');
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

})

app.controller('facultyManager', function ($scope, $rootScope, $http) {
   $rootScope.bcrumb1 = 'Faculty Manager';
   console.log('faculty manager page');

   // Getting instructors from the API and storing it into the instructors var
   $scope.instructors = [];
   $scope.getInstructors = function () {
      $http({
         method: 'GET',
         url: '/get/instructors',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.instructors = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the function
   $scope.getInstructors();

})

app.controller('facultyPreferences', function ($scope, $rootScope, $http, $routeParams) {
   $rootScope.bcrumb1 = 'Faculty Manager';
   $rootScope.bcrumb1Link = '#facultyManager';
   $rootScope.bcrumb2 = 'Faculty Preferences';


   // Getting preferences from the API and storing it into the preferences var
   $scope.preferences = [];
   $scope.getPreferences = function () {
      $http({
         method: 'GET',
         url: '/get/preferences',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.preferences = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the function
   $scope.getPreferences();

   $scope.faculty_id = $routeParams.faculty_id;
   $scope.day = 'M'; // Starting day value is Monday

   $scope.formGroupID = 1;
   

})

app.controller('generateSchedule', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';
   $rootScope.bcrumb1Link = '#schedules';
   $rootScope.bcrumb2 = 'Current Schedule';
})

app.directive('fileModel', ['$parse', function ($parse) {
   return {
      restrict: 'A',
      link: function (scope, element, attrs) {
         var model = $parse(attrs.fileModel);
         var modelSetter = model.assign;

         element.bind('change', function () {
            scope.$apply(function () {
               modelSetter(scope, element[0].files[0]);
            });
         });
      }
   };
}]);

app.service('fileUpload', ['$http', function ($http) {
   this.uploadFileToUrl = function (file, uploadUrl) {
      var fd = new FormData();
      fd.append('file', file);

      $http.post(uploadUrl, fd, {
         transformRequest: angular.identity,
         headers: {
            'Content-Type': undefined
         }
      })

      .success(function () {
         console.log('worked file upload');
      })

      .error(function () {
         console.log('file upload did not work');
      });
   }
}]);

app.controller('importData', ['$scope', '$rootScope', 'fileUpload', function ($scope, $rootScope, fileUpload) {
   $rootScope.bcrumb1 = 'Import Data';
   $scope.uploadFile = function () {
      var file = $scope.myFile;

      console.log('file is ');
      console.dir(file);
      var filename = file.name;
      console.log('file name is ' + filename)

      if (filename.includes("Room")) {
         var uploadUrl = "/importRoomData";
      } else if (filename.includes("Historic")) {
         var uploadUrl = "/importHistoricData";
      } else if (filename.includes("Faculty")) {
         var uploadUrl = "/importFacultyData";
      } else if (filename.includes("Student")) {
         var uploadUrl = "/importStudentData";
      } else if (filename.includes("Cohort")) {
         var uploadUrl = "/importCohortData";
      } else if (filename.includes("Course")) {
         var uploadUrl = "/importCourseData";
      }

      fileUpload.uploadFileToUrl(file, uploadUrl);
   };
}]);


app.controller('notifications', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Notifications';
})

app.controller('roomManager', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Room Manager';

})

app.controller('schedules', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';

})

app.controller('viewSchedule', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';
   $rootScope.bcrumb1Link = '#schedules';
   $rootScope.bcrumb2 = 'Current Schedule';
})
