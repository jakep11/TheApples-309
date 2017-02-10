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
    $scope.radioSelected = false;

  $scope.radioChanged = function(course) {
    $scope.current = {
      'id' : course.id,
      'number' : course.number,
      'major' : course.major,
      'lecture_workload_units' : course.lecture_workload_units,
      'lecture_hours' : course.lecture_hours,
      'lab_workload_units' : course.lab_workload_units,
      'lab_hours' : course.lab_hours
    }
    $scope.radioSelected = true;

  }
  $scope.openEdit = function() {
    $scope.edit = $scope.current;
  }

  $scope.addCourse = function() {
    $http({
      method: 'POST',
      url: '/create/course',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
       'major': $scope.new.major,
       'number': $scope.new.number,
       'lecture_workload_units' : $scope.new.lecture_workload_units,
      'lecture_hours' : $scope.new.lecture_hours,
      'lab_workload_units' : $scope.new.lab_workload_units,
      'lab_hours' : $scope.new.lab_hours
     }
   }).then(function successCallback(response) {
     $window.location.reload();
   }, function errorCallback(response) {
     console.log('error');
   });
 }

 $scope.editCourse = function() {
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
       'lecture_workload_units' : $scope.edit.lecture_workload_units,
      'lecture_hours' : $scope.edit.lecture_hours,
      'lab_workload_units' : $scope.edit.lab_workload_units,
      'lab_hours' : $scope.edit.lab_hours
    }
  }).then(function successCallback(response) {
    console.log('Calling edit course');
    $window.location.reload();
  }, function errorCallback(response) {
   console.log('error');
 });
}

$scope.deleteCourse = function() {
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

app.controller('facultyManager', function ($scope, $rootScope) {
    $rootScope.bcrumb1 = 'Faculty Manager';
    console.log('faculty manager page');

})

app.controller('facultyPreferences', function ($scope, $rootScope) {
    $rootScope.bcrumb1 = 'Faculty Manager';
    $rootScope.bcrumb1Link = '#facultyManager';
    $rootScope.bcrumb2 = 'Faculty Preferences';
})

app.controller('generateSchedule', function ($scope, $rootScope) {
    $rootScope.bcrumb1 = 'Schedules';
    $rootScope.bcrumb1Link = '#schedules';
    $rootScope.bcrumb2 = 'Current Schedule';
})

         app.directive('fileModel', ['$parse', function ($parse) {
            return {
               restrict: 'A',
               link: function(scope, element, attrs) {
                  var model = $parse(attrs.fileModel);
                  var modelSetter = model.assign;

                  element.bind('change', function(){
                     scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                     });
                  });
               }
            };
         }]);

         app.service('fileUpload', ['$http', function ($http) {
            this.uploadFileToUrl = function(file, uploadUrl){
               var fd = new FormData();
               fd.append('file', file);

               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
        })

        .success(function(){
        console.log('worked file upload');
        })

        .error(function(){
        console.log('file upload did not work');
        });
    }
}]);

         app.controller('importData', ['$scope', 'fileUpload', function($scope, fileUpload){
            $scope.uploadFile = function(){
               var file = $scope.myFile;

               console.log('file is ' );
               console.dir(file);


               var uploadUrl = '/importStudentData';
               fileUpload.uploadFileToUrl(file, uploadUrl);
            };
         }]);

//app.controller('importData', function ($scope, $rootScope) {
//    $rootScope.bcrumb1 = 'Import Data';
//
//    $scope.uploadFile = function () {
//        var file = $scope.myFile;
//
//        console.log('file is ');
//        console.dir(file);
//
//        var uploadUrl = '/fileUpload';
//        fileUpload.uploadFileToUrl(file, uploadUrl);
//        //$location.path()
//    }
//})


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
