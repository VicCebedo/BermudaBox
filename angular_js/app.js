'use strict';

var controllerSignup = angular.module('NoMsg.signup', []);

var app = angular.module('NoMsg', [
    'ngRoute',
    'NoMsg.signup'
    ]);

app.config(function($routeProvider){
    $routeProvider
    .when('/signup', {
        templateUrl: signup.html
    })
    .otherwise({
        redirectTo: '/signup'
    })
});