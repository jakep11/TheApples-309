//Initialize the angular application for this javascript page
var app = angular.module('TheApples');

//Each controller states what the breadcrumb for the page should be

app.controller('chairHome', function ($scope, $rootScope, $location, $cookies, $http) {
   $rootScope.bcrumb1 = null;

   $scope.numNotifications = 12;
   $scope.getNotifications = function () {
      $http({
         method: 'GET',
         url: '/get/comments',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         $scope.notifications = response.data;
         $scope.numNotifications = response.data.length;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the getComments function
   $scope.getNotifications();

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

   // get the faculty willing to teach the given course
   $scope.getSuitableFaculty = function (courseID) {
      $http({
         method: 'POST',
         url: '/get/facultyFromCourse',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'courseID': courseID
         }
      }).then(function successCallback(response) {
         $scope.ableFaculty = response.data;
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // get the rooms suitable for a course - currently gets all rooms
   $scope.getSuitableRooms = function () {
      $http({
         method: 'GET',
         url: 'get/rooms',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.suitableRooms = response.data;
         console.log("success");
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // call functions used to dynamically populate suitable resources for selected course
   $scope.getSuitableResources = function (courseID) {
      $scope.getSuitableFaculty(courseID);
      $scope.getSuitableRooms();
   }

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

   // Adds a user-specified course to the database
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

   // Edits a course in the database based on user-specified information
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

   // Removes a course from the database
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

   // Adds a faculty member to the database given user-specified data
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

app.controller('facultyPreferences', function ($scope, $rootScope, $http, $routeParams, $window, sharedData) {
   $rootScope.bcrumb1 = 'Faculty Manager';
   $rootScope.bcrumb1Link = '#facultyManager';
   $rootScope.bcrumb2 = 'Faculty Preferences';
   if ($rootScope.role == 'faculty') {
      $rootScope.bcrumb1 = 'Preferences';
      $rootScope.bcrumb1Link = null;
      $rootScope.bcrumb2 = null;
   }


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

   // Filtering displayed courses, updating the coursePreferences var
   $scope.plusButtonClicked = function () {
      $http({
         method: 'POST',
         url: '/get/filterCourses',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'filter': $scope.filter
         }
      }).then(function successCallback(response) {
         console.log($scope.filter);
         $scope.coursePreferences = response.data;
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // Saving any changes made to a faculty's time preferences
   $scope.changeTime = function () {

      $http({
         method: 'POST',
         url: '/edit/facultyPreference',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'time_pref': this.time_pref, // Using 'this' because of ng-repeat scope
            'p_id': this.preference.id
         }
      }).then(function successCallback(response) {
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });

   }

   // Saving any changes made to a faculty's course preferences.
   $scope.changePref = function () {
      $http({
         method: 'POST',
         url: '/edit/facultyCoursePreference',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'pref': this.pref, // Using 'this' because of ng-repeat scope
            'cp_id': this.coursePreference.id
         }
      }).then(function successCallback(response) {
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // Saving changes when 'save' is clicked. Faculty work units, and comments updated/saved.
   $scope.saveChanges = function () {
      $http({
         method: 'POST',
         url: '/edit/saveChanges',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'comment': $scope.comment,
            'time': new Date().toLocaleString(),
            'unread': "true",
            'type': "Comment",
            'min_units': $scope.min_units,
            'max_units': $scope.max_units,
            'id': $scope.faculty_id
         }
      }).then(function successCallback(response) {
         $window.location.reload();
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
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
            'userID': parseInt($rootScope.user_id)
         }
      }).then(function successCallback(response) {
         sharedData.faculty = response.data;
         $scope.faculty_id = sharedData.faculty.id;
         console.log(sharedData.faculty);
         console.log("success");
      }, function errorCallback(response) {
         console.log("error");
      });
   }


   console.log(sharedData.faculty);
   //If faculty id isn't provided in the Url then check user vs faculty for id
   if ($routeParams.faculty_id) {
      $scope.faculty_id = $routeParams.faculty_id;
   } else {
      $scope.getFacultyFromUser();
   }
   $scope.day = 'M'; // Starting day value is Monday

   $scope.formGroupID = 1;


})

app.controller('generateSchedule', function ($scope, $rootScope, $http, $location, sharedData, $window) {
   $rootScope.bcrumb1 = 'Schedules';
   $rootScope.bcrumb1Link = '#schedules';
   $rootScope.bcrumb2 = 'Current Schedule';

   $scope.currentTerm = $location.search().term;
   $scope.startTimes = sharedData.startTimes;
   $scope.endTimes = sharedData.endTimes;
   $scope.schedule = null;

   $scope.getTerm = function() {
      $http({
            method: 'POST',
            url: '/get/term',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
               term_id: parseInt($scope.currentTerm)
            }
        }).then(function successCallback(response) {
            $scope.term = response.data;
            $scope.published = response.data.published;
        }, function errorCallback(response) {
            console.log('error');
        });
   }
   $scope.getTerm();

   $scope.publishTerm = function(pub) {
      $http({
            method: 'POST',
            url: '/edit/term',
            headers: {
                'Content-Type': 'application/json'
            },
            data: {
               id: $scope.term.id,
               published: pub
            }
        }).then(function successCallback(response) {
            console.log($scope.term);
            $window.location.reload();

        }, function errorCallback(response) {
            console.log('error');
        });
   }

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
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getTerms();

    $scope.getFaculty = function () {
        $http({
            method: 'GET',
            url: '/get/instructors',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.faculty = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getFaculty();

    $scope.getRooms = function () {
        $http({
            method: 'GET',
            url: '/get/rooms',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function successCallback(response) {
            $scope.rooms = response.data;
            console.log('success');
        }, function errorCallback(response) {
            console.log('error');
        });
    }
    $scope.getRooms();

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

   $scope.getSections = function () {
      console.log($scope.currentTerm);
      console.log("hi");
      $http({
         method: 'POST',
         url: 'filter/sections',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'terms': [parseInt($scope.currentTerm)]
         }
      }).then(function successCallback(response) {
         $scope.sections = response.data;
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getSections();

   $scope.radioSelected = false;

   $scope.radioChanged = function (section) {
      console.log(section);
      $scope.current = {
         'id': section.id,
         'course': section.course,
         'course_id': section.course_id,
         'course_num': section.course_num,
         'term_id': section.term_id,
         'faculty': section.faculty,
         'faculty_id': section.faculty_id,
         'room': section.room,
         'room': section.room_id,
         'number': section.number,
         'section_type': section.section_type,
         'time_start': section.time_start,
         'time_end': section.time_end,
         'hours': section.hours,
         'days': section.days,
         'capacity': section.capacity

      }
      $scope.radioSelected = true;
      console.log($scope.current);

   }
   $scope.openEdit = function () {
      $scope.edit = $scope.current;
      console.log($scope.current);
   }


   // Adds a section to the database
   $scope.addSection = function () {
      console.log($scope.add.time_start);
      $http({
         method: 'POST',
         url: 'create/section',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            course_id: parseInt($scope.add.course_id),
            term_id: parseInt($scope.currentTerm),
            faculty_id: parseInt($scope.add.faculty_id),
            room_id: parseInt($scope.add.room_id),
            number: $scope.add.sectionNumber,
            section_type: $scope.add.compType,
            time_start: parseInt($scope.add.time_start),
            time_end: parseInt($scope.add.time_end),
            days: $scope.add.days
         }
      }).then(function successCallback(response) {
         console.log("Section added");
         $window.location.reload();
      }, function errorCallback(response) {
         if (response.status == 406) {
            alert("Room Time Conflict. Unable to add section.");
         }
         if (response.status == 405) {
            alert("Faculty Time Conflict. Unable to add section.");
         }
         if (response.status == 403) {
            alert("Faculty Workload Units Exceeded. Unable to add section.");
         }
         console.log('error');
      });
   }

   // Edits a section in the database
   $scope.editSection = function () {
      $http({
         method: 'POST',
         url: 'edit/section',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            id: parseInt($scope.edit.id),
            course_id: parseInt($scope.edit.course_id),
            term_id: parseInt($scope.currentTerm),
            faculty_id: parseInt($scope.edit.faculty_id),
            room_id: parseInt($scope.edit.room_id),
            number: $scope.edit.sectionNumber,
            section_type: $scope.edit.compType,
            time_start: $scope.edit.time_start,
            time_end: $scope.edit.time_end,
            days: $scope.edit.days
         }
      }).then(function successCallback(response) {
         console.log("Section edited");
         $window.location.reload();
      }, function errorCallback(response) {
         if (response.status == 406) {
            alert("Room Conflict");
         }
         if (response.status == 405) {
            alert("Faculty Conflict");
         }
         console.log('error');
      });
   }

   // Removes a section from the database
   $scope.deleteSection = function () {
      $http({
         method: 'POST',
         url: 'delete/section',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            id: $scope.current.id
         }
      }).then(function successCallback(response) {
         console.log("Section deleted");
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }



})

// Needed in order to upload a CSV file to the server in order to use it in the backend
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

// Uploads a CSV file to the server so that it's information can be parsed through in Flask
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

   // This function figures out which kind of CSV file is being imported into the system based on the
   // name of the file, and calls the corresponding importCSV python function in order to add the
   // included information to the right tables in the database
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

   // Gets all the imported filenames from the database to be displayed on the ImportCSV page
   $scope.getFileNames = function () {
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


app.controller('notifications', function ($scope, $rootScope, $http, $window, $route) {
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

   // The function gets the entire message of the selected comment
   $scope.readMore = function () {
      var selectedComment = this.selectedComment;

      // Find the existing comment
      for (var i in $scope.comments) {
         if ($scope.comments[i].id == selectedComment) {
            console.log("The selected comment has been found");
            $scope.popUpMessage = $scope.comments[i].comment;
         }
      }

   }

   // Changes comment.unread from true to false. Calling this function will change the color of the message
   // on the notifications page.
   $scope.markAsRead = function () {
      console.log("made it to mark as read");
      $http({
         method: 'POST',
         url: '/edit/comment',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'id': this.selectedComment,
            'unread': false
         }
      }).then(function successCallback(response) {
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
      $route.reload();
   }

   // Changes comment.unread from true to false. Calling this function will change the color of the message
   // on the notifications page.
   $scope.markAsUnread = function () {
      $http({
         method: 'POST',
         url: '/edit/comment',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            'id': this.selectedComment,
            'unread': true
         }
      }).then(function successCallback(response) {
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
      $route.reload();
   }

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

   // Gets all of the roomtypes from the database
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

   // Adds a roomtype to the database
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

   // Removes a roomtype from the database
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
   $scope.roomTypeRadioChanged = function (id) {
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

   // Adds a room to the database
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
            'type': $scope.add.type,
            'equipment': $scope.add.equipment,
            'comments': $scope.add.comments
         }
      }).then(function successCallback(response) {
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // Edits a room in the database
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
            'type': $scope.edit.type,
            'equipment': $scope.edit.equipment,
            'comments': $scope.edit.comments
         }
      }).then(function successCallback(response) {
         console.log('Calling edit Room');
         $window.location.reload();
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   // Removes a room from the database
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

app.controller('schedules', function ($scope, $rootScope, $http, $window) {
   $rootScope.bcrumb1 = 'Schedules';

   $scope.terms = [];
   $scope.getTerms = function () {
      $http({
         method: 'GET',
         url: '/get/terms',
         headers: {
            'Content-Type': "application/json"
         }
      }).then(function successCallback(response) {
         console.log("success");
         console.log(response.data);
         $scope.terms = response.data;
      }, function errorCallback(response) {
         console.log("error");
      });
   }

   // Calling the function
   $scope.getTerms();

   $scope.radioSelected = false;

// Handles keeping track of which schedule radio button is selected
$scope.radioChanged = function (term) {
   console.log(term);
   $scope.current = {
      'id': term.id,
      'quarter': term.name,
      'year': parseInt(term.year),
      'published': "0"
      
   }
   $scope.radioSelected = true;
   console.log("current set");

}
$scope.openEdit = function () {
   $scope.edit = $scope.current;
   console.log($scope.current);
}

// Adds a schedule to the database
$scope.addTerm = function () {
   $http({
      method: 'POST',
      url: '/create/term',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'name': $scope.quarter + " " + $scope.year,
      }
   }).then(function successCallback(response) {
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

// Edits a schedule in the database
$scope.editTerm = function () {
   $http({
      method: 'POST',
      url: '/edit/term',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.edit.id,
         'name': $scope.edit.quarter + " " + $scope.edit.year
      }
   }).then(function successCallback(response) {
      console.log('Calling edit Term');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

// Removes a schedule from the database
$scope.deleteTerm = function () {
   console.log("trying to delete schedule");
   $http({
      method: 'POST',
      url: '/delete/term',
      headers: {
         'Content-Type': 'application/json'
      },
      data: {
         'id': $scope.current.id
      }
   }).then(function successCallback(response) {
      console.log('Calling delete term');
      $window.location.reload();
   }, function errorCallback(response) {
      console.log('error');
   });
}

})

app.controller('viewSchedule', function ($scope, $rootScope) {
   $rootScope.bcrumb1 = 'Schedules';
   $rootScope.bcrumb1Link = '#schedules';
   $rootScope.bcrumb2 = 'Current Schedule';
})

app.controller('historicData', function ($scope, $rootScope, $http) {
   $rootScope.bcrumb1 = 'Historic Data';

   $scope.getScheduleFinal = function (term) {
      $http({
         method: 'POST',
         url: '/get/scheduleFinal',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            term: term
         }
      }).then(function successCallback(response) {
         $scope.historicData = response.data;
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.getTerms = function () {
      $http({
         method: 'GET',
         url: '/get/historicDataTerms',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.terms = response.data;
         $scope.currentTerm = $scope.terms[0].name;
         $scope.getScheduleFinal($scope.currentTerm);
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getTerms();

   $scope.selectTerm = function () {
      console.log("Select term");
      $scope.getScheduleFinal($scope.currentTerm);

   }

})

app.controller('planningData', function ($scope, $rootScope, $http) {
   $rootScope.bcrumb1 = 'Planning Data';

   $scope.getPlanningData = function (term) {
      $http({
         method: 'POST',
         url: '/get/planningData',
         headers: {
            'Content-Type': 'application/json'
         },
         data: {
            term: term
         }
      }).then(function successCallback(response) {
         $scope.planningData = response.data;
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }

   $scope.getTerms = function () {
      $http({
         method: 'GET',
         url: '/get/planningDataTerms',
         headers: {
            'Content-Type': 'application/json'
         }
      }).then(function successCallback(response) {
         $scope.terms = response.data;
         $scope.currentTerm = $scope.terms[0].name;
         $scope.getPlanningData($scope.currentTerm);
         console.log('success');
      }, function errorCallback(response) {
         console.log('error');
      });
   }
   $scope.getTerms();

   $scope.selectTerm = function () {
      console.log("Select term");
      $scope.getPlanningData($scope.currentTerm);
   }

})
