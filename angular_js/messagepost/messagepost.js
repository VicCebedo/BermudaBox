'use strict';

angular.module('NoMsg.message_post', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/messagepost', {
    templateUrl: 'signup/signup.html',
    controller: 'SignupCtrl'
  });
}])
.controller('SignupCtrl', function($scope, $http){

    // If the submit button is pressed.
    $scope.submit = function() {

        // Send a POST to:
        // @app.route('/user/<user_name>/', methods=['POST'])
        var username = $scope.inputUsername;
        var url = "http://127.0.0.1:5000/user/"+username+"/";

        $http.post(url)
        .then(function(response){
            $scope.responseData = response.data;
        });
    };
});