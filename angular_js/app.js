'use strict';

// Declare app level module which depends on views, and components
angular.module('NoMsg', [
  'ngRoute',
  'NoMsg.home',
  'NoMsg.messagepost',
  'NoMsg.messagepostanon',
  'NoMsg.messagegetall',
  'NoMsg.signup'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider
  .otherwise({redirectTo: '/'});
}]);
