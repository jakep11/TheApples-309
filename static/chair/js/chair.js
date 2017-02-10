var app = angular.module('TheApples')


app.controller("chairHome", function ($scope, $rootScope, $location, $cookies) {
    $rootScope.bcrumb1 = null;

    $scope.numNotifications = 12;

    $scope.logout = function () {
        console.log("logging out");
        $location.path("/login");
    }


})

app.controller("courseManager", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Course Manager";
})

app.controller("facultyManager", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Faculty Manager";
    console.log("faculty manager page");

})

app.controller("facultyPreferences", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Faculty Manager";
    $rootScope.bcrumb1Link = "#facultyManager";
    $rootScope.bcrumb2 = "Faculty Preferences";
})

app.controller("generateSchedule", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Schedules";
    $rootScope.bcrumb1Link = "#schedules";
    $rootScope.bcrumb2 = "Current Schedule";
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
        console.log("worked file upload");
        })

        .error(function(){
        console.log("file upload didn't work");
        });
    }
}]);

app.controller('importData', ['$scope', 'fileUpload', function($scope, fileUpload){
    $scope.uploadFile = function(){
        var file = $scope.myFile;

        console.log('file is ' );
        console.dir(file);
        var filename = file.name;
        console.log('file name is ' + filename)

        if (filename.includes("Room")) {
            var uploadUrl = "/importRoomData";
        }

        else if (filename.includes("Historic")) {
            var uploadUrl = "/importHistoricData";
        }

        else if (filename.includes("Student")) {
            var uploadUrl = "/importStudentData";
        }

        else if (filename.includes("Cohort")) {
            var uploadUrl = "/importCohortData";
        }

        else if (filename.includes("Course")) {
            var uploadUrl = "/importCourseData";
        }

        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
}]);


app.controller("notifications", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Notifications";
})

app.controller("roomManager", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Room Manager";

})

app.controller("schedules", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Schedules";

})

app.controller("viewSchedule", function ($scope, $rootScope) {
    $rootScope.bcrumb1 = "Schedules";
    $rootScope.bcrumb1Link = "#schedules";
    $rootScope.bcrumb2 = "Current Schedule";
})
