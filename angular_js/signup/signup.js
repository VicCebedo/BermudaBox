'use strict';

angular.module('NoMsg.signup', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signup', {
    templateUrl: 'signup/signup.html',
    controller: 'SignupCtrl'
  });
}])

.controller('SignupCtrl', [function() {

}]);
