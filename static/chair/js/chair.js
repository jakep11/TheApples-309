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

app.controller("importData", function ($scope, $rootScope, fileUpload) {
    $rootScope.bcrumb1 = "Import Data";


    $scope.uploadFile = function () {
        var file = $scope.myFile;

        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    }
})

// UPLOADING FILES
//
//app.directive('fileModel', ['$parse', function ($parse) {
//    return {
//        restrict: 'A',
//        link: function (scope, element, attrs) {
//            var model = $parse(attrs.fileModel);
//            var modelSetter = model.assign;
//
//            element.bind('change', function () {
//                scope.$apply(function () {
//                    modelSetter(scope, element[0].files[0]);
//                });
//            });
//        }
//    };
//}])
//
//app.service('fileUpload', ['$https:', function ($https: ) {
//    this.uploadFileToUrl = function (file, uploadUrl) {
//        var fd = new FormData();
//        fd.append('file', file);
//
//        $https: .post(uploadUrl, fd, {
//            transformRequest: angular.identity,
//            headers: {
//                'Content-Type': undefined
//            }
//        })
//
//        .success(function () {})
//
//        .error(function () {});
//    }
//}])

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
