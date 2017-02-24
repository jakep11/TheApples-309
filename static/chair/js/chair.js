var app = angular.module('TheApples');


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
   $scope.getComponents = function () {
      $http({
         method: 'GET',
         url: 'get/allComponents',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.components = response.data;
         console.log($scope.components);
         console.log('success');
         combineCoursesComponents();
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getComponents();

   $scope.getComponentTypes = function () {
      $http({
         method: 'GET',
         url: 'get/componentTypes',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.componentTypes = response.data;
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getComponentTypes();

   $scope.addComponentType = function () {
      $http({
         method: 'POST',
         url: 'create/componentType',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            name: $scope.addComponent
         }
      }).then(function successCallback(response) {
         console.log("Component added");
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.removeComponentType = function () {
      $http({
         method: 'POST',
         url: 'delete/componentType',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            id: $scope.selectedComponentType
         }
      }).then(function successCallback(response) {
         console.log("Component deleted");
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.compTypeRadioSelected = false;
   $scope.compTypeRadioChanged = function (id) {
      $scope.selectedComponentType = id;
      $scope.compTypeRadioSelected = true;

   }


   //Combining courses and components list into one..
   function combineCoursesComponents() {

      var arrayList = [];
      var courses = $scope.courses;
      var comps = $scope.components;
      for (var i in courses) {
         var obj = {
            id: courses[i].id,
            number: courses[i].number,
            major: courses[i].major,
            course_name: courses[i].course_name
         };

         for (var j in comps) {
            if (courses[i].id == comps[j].course_id) {
               if (obj.component_one != null) {
                  obj.component_two = comps[j].name;
                  obj.c2_workload_units = comps[j].workload_units;
                  obj.c2_hours = comps[j].hours;
               } else {
                  obj.component_one = comps[j].name;
                  obj.c1_workload_units = comps[j].workload_units;
                  obj.c1_hours = comps[j].hours;
               }

            }
         }
         obj.c1_workload_units = obj.c1_workload_units || null;
         obj.c1_hours = obj.c1_hours || null;
         obj.c2_workload_units = obj.c2_workload_units || null;
         obj.c2_hours = obj.c2_hours || null;
         obj.component_one = obj.component_one || null;
         obj.component_two = obj.component_two || null;
         arrayList.push(obj);

      }
      console.log(arrayList);
      $scope.courses = arrayList;
   }


   $scope.radioSelected = false;

   $scope.radioChanged = function (course) {
      $scope.current = {
         'id': course.id,
         'number': course.number,
         'major': course.major,
         'course_name': course.course_name,
         'component_one': course.component_one,
         'c1_workload_units': course.c1_workload_units,
         'c1_hours': course.c1_hours,
         'component_two': course.component_two,
         'c2_workload_units': course.c2_workload_units,
         'c2_hours': course.c2_hours
      }
      $scope.radioSelected = true;
      console.log("current set");

   }
   $scope.openEdit = function () {
      $scope.edit = $scope.current;
      console.log($scope.current);
   }


   $scope.addCourse = function () {
      $http({
         method: 'POST',
         url: '/create/course',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'major': $scope.add.major,
            'number': $scope.add.number,
            'course_name': $scope.add.course_name,
            'component_one': $scope.add.c1,
            'c1_workload_units': $scope.add.c1_workload_units,
            'c1_hours': $scope.add.c1_hours,
            'component_two': $scope.add.c2,
            'c2_workload_units': $scope.add.c2_workload_units,
            'c2_hours': $scope.add.c2_hours
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
         url: '/edit/course',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'id': $scope.edit.id,
            'major': $scope.edit.major,
            'number': $scope.edit.number,
            'course_name': $scope.edit.course_name,
            'component_one': $scope.edit.component_one,
            'c1_workload_units': $scope.edit.c1_workload_units,
            'c1_hours': $scope.edit.c1_hours,
            'component_two': $scope.edit.component_two,
            'c2_workload_units': $scope.edit.c2_workload_units,
            'c2_hours': $scope.edit.c2_hours
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

app.controller('facultyManager', function ($scope, $rootScope, $http, $window) {
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

   $scope.radioSelected = false;

$scope.radioChanged = function (faculty) {
   console.log(faculty);
   $scope.current = {
      'id': faculty.id,
      'first_name': faculty.first_name,
      'last_name': faculty.last_name,
      'min_work_units': faculty.min_work_units,
      'max_work_units': faculty.max_work_units
      
   }
   $scope.radioSelected = true;
   console.log("current set");

}
$scope.openEdit = function () {
   $scope.edit = $scope.current;
   console.log($scope.current);
}


$scope.addFaculty = function () {
   $http({
      method: 'POST',
      url: '/create/faculty',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'first_name': $scope.add.first_name,
         'last_name': $scope.add.last_name,
         'max_work_units': $scope.add.max_work_units,
         'min_work_units': $scope.add.min_work_units
      }
   }).then(function successCallback(response) {
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

$scope.editFaculty = function () {
   $http({
      method: 'POST',
      url: '/edit/faculty',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.edit.id,
         'first_name': $scope.edit.first_name,
         'last_name': $scope.edit.last_name,
         'max_work_units': $scope.edit.max_work_units,
         'min_work_units': $scope.edit.min_work_units
      }
   }).then(function successCallback(response) {
      console.log('Calling edit Faculty');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

$scope.deleteFaculty = function () {
   console.log("trying to delete faculty");
   $http({
      method: 'POST',
      url: '/delete/faculty',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.current.id
      }
   }).then(function successCallback(response) {
      console.log('Calling delete faculty');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}


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

   // Calling getPreference function
   $scope.getPreferences();


   // Getting course_preferences from the API and storing it into the coursePreferences var
   $scope.coursePreferences;
   $scope.getCoursePreferences = function () {
      $http({
         method: 'GET',
         url: '/get/coursePreferences',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.coursePreferences = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling getCoursePreference function
   $scope.getCoursePreferences();



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

app.controller('importData', ['$scope', '$rootScope', 'fileUpload', '$http', function ($scope, $rootScope, fileUpload, $http) {
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
      } else if (filename.includes("Equipment")) {
         var uploadUrl = "/importEquipData";
      }

      fileUpload.uploadFileToUrl(file, uploadUrl);
      console.log("done uploading file");
   };

   $scope.getFileNames = function() {
      $http({
         method: 'GET',
         url: '/get/fileNames',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         $scope.fileNames = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }
   $scope.getFileNames();

}]);


app.controller('notifications', function ($scope, $rootScope, $http, $window) {
   $rootScope.bcrumb1 = 'Notifications';

   // Getting notifications from the API and storing it into the notifications var
   $scope.comments = [];
   $scope.getNotifications = function () {
      $http({
         method: 'GET',
         url: '/get/comments',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.comments = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the getComments function
   $scope.getNotifications();

})

app.controller('roomManager', function ($scope, $rootScope, $http, $window) {
   $rootScope.bcrumb1 = 'Room Manager';

   // Getting instructors from the API and storing it into the instructors var
   $scope.rooms = [];
   $scope.getRooms = function () {
      $http({
         method: 'GET',
         url: '/get/rooms',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.rooms = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the function
   $scope.getRooms();

   $scope.getRoomTypes = function () {
      $http({
         method: 'GET',
         url: 'get/roomTypes',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.roomTypes = response.data;
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getRoomTypes();

   $scope.addRoomType = function () {
      $http({
         method: 'POST',
         url: 'create/roomType',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            name: $scope.newRoomType
         }
      }).then(function successCallback(response) {
         console.log("Room added");
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.removeRoomType = function () {
      $http({
         method: 'POST',
         url: 'delete/roomType',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            id: $scope.selectedRoomType
         }
      }).then(function successCallback(response) {
         console.log("Room deleted");
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.roomTypeRadioSelected = false;
  $scope.roomTypeRadioChanged = function(id) {
    $scope.selectedRoomType = id;
    $scope.roomTypeRadioSelected = true;

  }

$scope.radioSelected = false;

$scope.radioChanged = function (room) {
   console.log(room);
   $scope.current = {
      'id': room.id,
      'number': room.number,
      'capacity': room.capacity,
      'type': room.type
      
   }
   $scope.radioSelected = true;
   console.log("current set");

}
$scope.openEdit = function () {
   $scope.edit = $scope.current;
   console.log($scope.current);
}


$scope.addRoom = function () {
   $http({
      method: 'POST',
      url: '/create/room',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'number': $scope.add.number,
         'capacity': $scope.add.capacity,
         'type': $scope.add.type
      }
   }).then(function successCallback(response) {
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

$scope.editRoom = function () {
   $http({
      method: 'POST',
      url: '/edit/room',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.edit.id,
         'number': $scope.edit.number,
         'capacity': $scope.edit.capacity,
         'type': $scope.edit.type
      }
   }).then(function successCallback(response) {
      console.log('Calling edit Room');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

$scope.deleteRoom = function () {
   console.log("trying to delete room");
   $http({
      method: 'POST',
      url: '/delete/room',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.current.id
      }
   }).then(function successCallback(response) {
      console.log('Calling delete room');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

})

app.controller('schedules', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';

})

app.controller('viewSchedule', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';
   $rootScope.bcrumb1Link = '#schedules';
   $rootScope.bcrumb2 = 'Current Schedule';
})
