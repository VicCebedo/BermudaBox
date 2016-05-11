'use strict';

angular.module('NoMsg.signup', ['ngRoute', 'vcRecaptcha'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signup', {
    templateUrl: 'signup/signup.html',
    controller: 'SignupCtrl'
  });
}])
.controller('SignupCtrl', function($scope, $http, vcRecaptchaService){

    $scope.response = null;
    $scope.widgetId = null;
    $scope.model = {
        key: '6LcQgx8TAAAAAJ8zw9g5mDg8YQX_znHo_v7S7xM4'
    };

    $scope.setResponse = function (response) {
        console.info('Response available');
        $scope.response = response;
    };

    $scope.setWidgetId = function (widgetId) {
        console.info('Created widget ID: %s', widgetId);
        $scope.widgetId = widgetId;
    };

    $scope.cbExpiration = function() {
        console.info('Captcha expired. Resetting response object');
        vcRecaptchaService.reload($scope.widgetId);
        $scope.response = null;
    };

    // If the submit button is pressed.
    $scope.submit = function() {

        //URL: https://www.google.com/recaptcha/api/siteverify
        //secret (required)
        //response (required)

        // Check if the captcha was legit.
        var url = "http://127.0.0.1:5000/user/"+$scope.inputUsername+"/"
        var captchaData = [{"secret":"6LcQgx8TAAAAAGirYHjHNN7XOAGUN0q9okWmTnWD"}, {"response":$scope.response}];
        $http.post(url, captchaData)
        .then(function(response){
            // Display text response.
            vcRecaptchaService.reload($scope.widgetId);
            $scope.responseData = response.data;
        });
    };
});